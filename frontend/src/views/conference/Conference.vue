<template>
  <div class="conference">
    <!-- Local video -->
    <conference-video
      v-if="localStream"
      :uuid="username"
      :name="username"
      :stream="localStream"
      :styles="videoSize"
    />

    <!-- Other users videos -->
    <conference-video
      v-for="{uuid, name, stream} in videosData"
      :key="uuid"
      :uuid="uuid"
      :name="name"
      :stream="stream"
      :styles="videoSize"
      :buttonsPanel="true"
      @onClose="handleRemovePeer"
    />
  </div>
</template>

<script>
import { mapState } from 'vuex';
import ConferenceVideo from './ConferenceVideo.vue';

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

const getVideosCountBounds = videosCount => {
  let bound = 1;

  while (bound * bound < videosCount) {
    bound <<= 1;
  }

  return bound;
};

export default {
  components: { ConferenceVideo },
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
    },
    videoSize () {
      const localVideo = 1;
      const videosCount = localVideo + this.videosData.length;
      const videosCountBounds = getVideosCountBounds(videosCount);

      return {
        height: `calc(99vh / ${videosCountBounds})`,
        width: `calc(99vw / ${videosCountBounds})`,
        margin: '0.5vh 0'
      };
    }
  },
  methods: {
    updateVideo () {
      this.videosData = Object.entries(this.peerConnections)
        .map(([uuid, conn]) => ({
          uuid,
          name: conn.displayName,
          stream: conn.stream
        }))
        .filter(({ stream }) => Boolean(stream));
    },

    handleRemovePeer (uuid) {
      this.RTCServerConnection.send(JSON.stringify({
        forceDisconnect: true,
        uuid: this.username,
        peerToRemove: uuid,
        dest: 'all'
      }));
      this.cleanUpPeer(uuid);
    },

    async cleanUpPeer (uuid) {
      await this.peerConnections[uuid].pc.close();
      delete this.peerConnections[uuid];
      this.updateVideo();
    },

    closeConnection () {
      this.RTCServerConnection.close();
      this.RTCServerConnection = null;
      this.localStream.getTracks().forEach(track => track.stop());
      this.localStream = null;
      this.peerConnections = {};
      this.videosData = [];
    },

    async connect () {
      if (navigator.mediaDevices.getUserMedia) {
        try {
          this.localStream = await navigator.mediaDevices.getUserMedia(mediaConstraints);
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
      const signal = JSON.parse(message.data);
      const {
        uuid: peerUuid,
        dest,
        displayName,
        forceDisconnect,
        peerToRemove,
        sdp,
        ice
      } = signal;
      // Conditions
      const messageFromCurrentUser = peerUuid === this.username;
      const forbiddenMessage = (
        dest !== this.username &&
        dest !== 'all'
      );

      // Ignore messages that are not for us or from ourselves
      if (messageFromCurrentUser || forbiddenMessage) {
        return;
      }

      try {
        if (displayName && dest === 'all') {
          this.handleInitConnection({ peerUuid, displayName });
        } else if (peerToRemove && forceDisconnect && dest === 'all') {
          this.handleUserKick({ peerToRemove });
        } else if (displayName && dest === this.username) {
          this.setUpPeer({
            peerUuid,
            displayName: signal.displayName,
            initCall: true
          });
        } else if (sdp) {
          await this.handleSdpConnection({ peerUuid, sdp });
        } else if (ice) {
          await this.handleIceConnection({ peerUuid, ice });
        } else {
          console.log('Unknown message from server: ', signal);
        }
      } catch (error) {
        this.handleRTCError(error);
      }
    },

    handleInitConnection ({ peerUuid, displayName }) {
      // set up peer connection object for a newcomer peer
      this.setUpPeer({ peerUuid, displayName });

      this.RTCServerConnection.send(JSON.stringify({
        displayName: this.username,
        uuid: this.username,
        dest: peerUuid
      }));
    },

    handleUserKick ({ peerToRemove }) {
      // Remove user from all of the connections
      if (this.username === peerToRemove) {
        // Remove the connection for the user itself
        this.closeConnection();

        setTimeout(() => {
          alert('You were kicked from the conference!');
        }, 0);
      } else {
        // Remove user for other people
        this.cleanUpPeer(peerToRemove);
      }
    },

    async handleSdpConnection ({ peerUuid, sdp }) {
      await this.peerConnections[peerUuid].pc.setRemoteDescription(
        new RTCSessionDescription(sdp)
      );

      // Only create answers in response to offers
      if (sdp.type === 'offer') {
        const description = await this.peerConnections[peerUuid].pc.createAnswer();
        this.createDescription({ description, peerUuid });
      }
    },

    async handleIceConnection ({ peerUuid, ice }) {
      await this.peerConnections[peerUuid].pc.addIceCandidate(
        new RTCIceCandidate(ice)
      );
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
      const state = this.peerConnections[peerUuid].pc.iceConnectionState;
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
  #app {
    background-color: black;
  }

  *, ::before, ::after {
    box-sizing: content-box;
  }
</style>

<style lang="scss" scoped>
  .conference {
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-content: center;
    flex-wrap: wrap;
  }
</style>
