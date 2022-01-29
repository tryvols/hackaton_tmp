<template>
  <div class="conference">
    <div class="conference__video-container">
      <video class="conference__video" ref="localVideo" autoplay muted></video>
      <div class="conference__video-label">{{ username }}</div>
    </div>

    <div
      v-for="{uuid, name, stream} in videosData"
      :key="uuid"
      class="conference__video-container"
    >
      <video class="conference__video" autoplay muted :srcObject.prop="stream"></video>
      <div class="conference__video-label">{{ name }}</div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

const WS_PORT = 8443;

const peerConnectionConfig = {
  iceServers: [
    { urls: 'stun:stun.stunprotocol.org:3478' },
    { urls: 'stun:stun.l.google.com:19302' }
  ]
};

const mediaConstraints = {
  video: {
    width: { max: 320 },
    height: { max: 240 },
    frameRate: { max: 30 }
  },
  audio: true
};

export default {
  mounted () {
    this.connect();
  },
  data () {
    return {
      localStream: null,
      RTCServerConnection: null,
      peerConnections: {},
      videosData: []
    };
  },
  computed: {
    ...mapState('User', [
      'username'
    ]),
    conferenceCode () {
      return this.$route.params.code;
    }
  },
  methods: {
    updateVideo () {
      this.videosData = Object.entries(this.peerConnections)
        .map(([uuid, conn]) => {
          return {
            uuid,
            name: conn.displayName,
            stream: conn.stream
          };
        })
        .filter(({ stream }) => Boolean(stream));
      console.log(this.videosData);
    },

    async connect () {
      if (navigator.mediaDevices.getUserMedia) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia(mediaConstraints);
          this.localStream = stream;
          this.$refs.localVideo.srcObject = stream;
        } catch (error) {
          this.handleRTCError(error);
        }

        try {
          this.RTCServerConnection = new WebSocket('wss://' + window.location.hostname + ':' + WS_PORT);
          this.RTCServerConnection.onmessage = this.handleMessageFromServer;
          this.RTCServerConnection.onopen = event => {
            this.RTCServerConnection.send(JSON.stringify({
              displayName: this.username,
              uuid: this.username,
              dest: 'all'
            }));
          };
        } catch (error) {
          this.handleRTCError(error);
        }
      } else {
        alert('Your browser does not support getUserMedia API');
      }
    },

    async handleMessageFromServer (message) {
      var signal = JSON.parse(message.data);
      var peerUuid = signal?.uuid;

      // Ignore messages that are not for us or from ourselves
      if (peerUuid === this.username || (signal.dest !== this.username && signal.dest !== 'all')) return;

      try {
        if (signal.displayName && signal.dest === 'all') {
          // set up peer connection object for a newcomer peer
          this.setUpPeer({
            peerUuid,
            displayName: signal.displayName
          });

          this.RTCServerConnection.send(JSON.stringify({
            displayName: this.username,
            uuid: this.username,
            dest: peerUuid
          }));
        } else if (signal.displayName && signal.dest === this.username) {
          // initiate call if we are the newcomer peer
          this.setUpPeer({
            peerUuid,
            displayName: signal.displayName,
            initCall: true
          });
        } else if (signal.sdp) {
          await this.peerConnections[peerUuid].pc.setRemoteDescription(
            new RTCSessionDescription(signal.sdp)
          );

          // Only create answers in response to offers
          if (signal.sdp.type === 'offer') {
            const description = await this.peerConnections[peerUuid].pc.createAnswer();
            this.createDescription({ description, peerUuid });
          }
        } else if (signal.ice) {
          await this.peerConnections[peerUuid].pc.addIceCandidate(
            new RTCIceCandidate(signal.ice)
          );
        }
      } catch (error) {
        this.handleRTCError(error);
      }
    },

    async setUpPeer ({ peerUuid, displayName, initCall = false }) {
      this.peerConnections[peerUuid] = {
        displayName,
        pc: new RTCPeerConnection(peerConnectionConfig)
      };

      const { pc } = this.peerConnections[peerUuid];

      pc.onicecandidate = event => {
        this.gotIceCandidate({ event, peerUuid });
      };
      pc.ontrack = event => {
        this.gotRemoteStream({ event, peerUuid });
      };
      pc.oniceconnectionstatechange = event => {
        this.checkPeerDisconnect({ event, peerUuid });
      };

      pc.addStream(this.localStream);

      if (initCall) {
        try {
          const description = await pc.createOffer();
          this.createDescription({ description, peerUuid });
        } catch (error) {
          this.handleRTCError(error);
        }
      }
    },

    async createDescription ({ description, peerUuid }) {
      console.log(`got description, peer ${peerUuid}`);
      try {
        await this.peerConnections[peerUuid].pc.setLocalDescription(description);
        this.RTCServerConnection.send(JSON.stringify({
          sdp: this.peerConnections[peerUuid].pc.localDescription,
          uuid: this.username,
          dest: peerUuid
        }));
      } catch (error) {
        this.handleRTCError(error);
      }
    },

    gotIceCandidate ({ event, peerUuid }) {
      if (event.candidate === null) {
        return;
      }

      this.RTCServerConnection.send(JSON.stringify({
        ice: event.candidate,
        uuid: this.username,
        dest: peerUuid
      }));
    },

    gotRemoteStream ({ event, peerUuid }) {
      console.log(`got remote stream, peer ${peerUuid}`);
      this.peerConnections[peerUuid].stream = event.streams[0];
      this.updateVideo();
    },

    checkPeerDisconnect ({ peerUuid }) {
      var state = this.peerConnections[peerUuid].pc.iceConnectionState;
      console.log(`connection with peer ${peerUuid} ${state}`);
      if (state === 'failed' || state === 'closed' || state === 'disconnected') {
        delete this.peerConnections[peerUuid];
        this.updateVideo();
      }
    },

    handleRTCError (error) {
      console.log(error);
    }
  }
};
</script>

<style lang="scss">
  :root {
    --rowHeight: 49vh;
    --colWidth: 49vw;
  }

  #app {
    background-color: black;
    display: block;
  }

  *, ::before, ::after {
    box-sizing: content-box;
  }
</style>

<style lang="scss" scoped>
  .conference {
    display: grid;
    grid-gap: 5px;
    grid-auto-flow: row;

    grid-template-columns: repeat(auto-fit, minmax(var(--colWidth), 1fr)) ;

    &__video-container {
      position: relative;
      overflow: hidden;

      min-height: var(--rowHeight);
      min-width: var(--colWidth);
    }

    &__video {
      position: absolute;
      left: 0;
      bottom: 0;
      height: auto;
      width: 100%;
    }

    &__video-label {
      color: white;
      font: bold 18px Arial, Sans-Serif;
      line-height: 18px;
      height: 18px;

      background: rgba(0, 0, 0, 0.55);

      position: absolute;
      left: 0;
      bottom: 0;
      padding: 4px;
    }
  }
</style>
