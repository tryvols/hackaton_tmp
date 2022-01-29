<template>
  <div class="conference">
    <!-- Local video -->
    <conference-video
      v-if="localStream"
      :uuid="username"
      :name="username"
      :stream="localStream"
      :styles="videoSizeStyles"
    />

    <!-- Other users videos -->
    <conference-video
      v-for="{uuid, name, stream} in videosData"
      :key="uuid"
      :uuid="uuid"
      :name="name"
      :stream="stream"
      :styles="videoSizeStyles"
      :buttonsPanel="true"
      @onClose="handleRemovePeer"
    />

    <conference-controls-panel
      :enabledVideoByDefault="isEnabledVideoByDefault"
      :mutedByDefault="isMutedByDefault"
      @finishCall="leftThisCall"
      @mute="muteMicrophone"
      @unmute="unmuteMicrophone"
      @enableVideo="enableCamera"
      @disableVideo="disableCamera"
    />
  </div>
</template>

<script>
import { mapState } from 'vuex';
import ConferenceControlsPanel from './ConferenceControlsPanel.vue';
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
  components: {
    ConferenceVideo,
    ConferenceControlsPanel
  },
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
    isEnabledVideoByDefault () {
      return true;
    },
    isMutedByDefault () {
      return true;
    },
    conferenceCode () {
      return this.$route.params.code;
    },
    videoSizeStyles () {
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
    /**
     * Camera and microphone states
     */
    setMicrophoneState ({ muted }) {
      this.localStream.getAudioTracks()[0].enabled = !muted;
    },

    unmuteMicrophone () {
      this.setMicrophoneState({ muted: false });
    },

    muteMicrophone () {
      this.setMicrophoneState({ muted: true });
    },

    setCameraState ({ enabled }) {
      this.localStream.getVideoTracks()[0].enabled = enabled;
    },

    enableCamera () {
      this.setCameraState({ enabled: true });
    },

    disableCamera () {
      this.setCameraState({ enabled: false });
    },

    /**
     * Update videos array to show/hide videos when connection changes
     */
    updateVideo () {
      this.videosData = Object.entries(this.peerConnections)
        .map(([uuid, conn]) => ({
          uuid,
          name: conn.displayName,
          stream: conn.stream
        }))
        .filter(({ stream }) => Boolean(stream));
    },

    /**
     * Methods to remove connection
     */
    leftThisCall () {
      this.closeConnection();
      setTimeout(() => {
        alert('You left this call!');
      }, 10);
    },

    handleRemovePeer (uuid) {
      this.RTCServerConnection.send(JSON.stringify({
        forceDisconnect: true,
        uuid: this.username,
        peerToRemove: uuid,
        dest: 'all',
        channel: this.conferenceCode
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

    /**
     * Rood method to begin and configure connection
     */
    async connect () {
      if (navigator.mediaDevices.getUserMedia) {
        try {
          this.localStream = await navigator.mediaDevices.getUserMedia(mediaConstraints);
          this.setCameraState({ enabled: this.isEnabledVideoByDefault });
          this.setMicrophoneState({ muted: this.isMutedByDefault });
        } catch (error) {
          this.handleRTCError(error);
        }

        try {
          this.RTCServerConnection = new WebSocket('ws://' + window.location.hostname + ':' + WS_PORT);
          this.RTCServerConnection.onmessage = this.handleMessageFromServer;
          this.RTCServerConnection.onopen = event => {
            this.RTCServerConnection.send(JSON.stringify({
              displayName: this.username,
              uuid: this.username,
              dest: 'all',
              channel: this.conferenceCode
            }));
          };
        } catch (error) {
          this.handleRTCError(error);
        }
      } else {
        alert('Your browser does not support getUserMedia API');
      }
    },

    /**
     * Something like a router for web sockets messages
     */
    async handleMessageFromServer (message) {
      const signal = JSON.parse(message.data);
      const {
        uuid: peerUuid,
        dest,
        displayName,
        forceDisconnect,
        peerToRemove,
        sdp,
        ice,
        channel
      } = signal;
      // Conditions
      const messageFromCurrentUser = peerUuid === this.username;
      const forbiddenMessage = (
        dest !== this.username &&
        dest !== 'all'
      );
      const isCurrentChannel = channel === this.conferenceCode;

      // Ignore messages that are not for us or from ourselves
      if (messageFromCurrentUser || forbiddenMessage || !isCurrentChannel) {
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

    /**
     * Web sockets messages handlers and helpers for them
     */
    handleInitConnection ({ peerUuid, displayName }) {
      // set up peer connection object for a newcomer peer
      this.setUpPeer({ peerUuid, displayName });

      this.RTCServerConnection.send(JSON.stringify({
        displayName: this.username,
        uuid: this.username,
        dest: peerUuid,
        channel: this.conferenceCode
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
          dest: peerUuid,
          channel: this.conferenceCode
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
        dest: peerUuid,
        channel: this.conferenceCode
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
