import { v4 as uuidv4 } from "uuid";
import { asyncSleep } from "../utils/utils.js";

const WEBSOCKET_URI = eval(process.env.VUE_APP_WEBSOCKET_URL),
  WEBSOCKET_CONNECTION_TIMEOUT = process.env.VUE_APP_SERVER_CONNECT_TIMEOUT,
  WEBSOCKET_RECONNECTION_TIMEOUT = 5000,
  WEBSOCKET_REQUEST_TIMEOUT = process.env.VUE_APP_SERVER_REQUEST_TIMEOUT;

class Server {
  constructor() {
    this.ws = undefined;
    this.deferredMessages = [];
    this.awaitedMessages = {};
    this.listeners = [];
  }

  async connect() {
    try {
      await new Promise((resolve, reject) => {
        try {
          if (
            this.ws &&
            this.ws.readyState !== WebSocket.CLOSING &&
            this.ws.readyState !== WebSocket.CLOSED
          ) {
            this.ws.close();
          }

          this.ws = new WebSocket(WEBSOCKET_URI);

          this.ws.addEventListener("open", event => {
            resolve(event);
            for (let i = 0; i < this.deferredMessages.length; ++i) {
              this.deferredMessages[i].resolve();
            }
          });

          this.ws.addEventListener("close", event => {
            reject(event);
          });

          this.ws.addEventListener("error", event => {
            reject(event);
          });

          setTimeout(() => {
            reject("connection timeout");
          }, WEBSOCKET_CONNECTION_TIMEOUT);

          this.ws.addEventListener("message", event => {
            let message = JSON.parse(event.data);

            if (
              !("id" in message && "type" in message && "message" in message)
            ) {
              console.error("ERROR", "unknown request structure"); // !!!
            } else {
              if (message.type === "response") {
                if (message.id in this.awaitedMessages) {
                  this.awaitedMessages[message.id].resolve(message.message);
                  delete this.awaitedMessages[message.id];
                } else {
                  console.error("ERROR", "unknown request id"); // !!!
                }
              } else if (message.type === "notify") {
                for (let i = 0; i < this.listeners.length; ++i) {
                  if (this.listeners[i].type === message.message.type) {
                    this.listeners[i].handler(message.message);
                  }
                }
              } else {
                console.error("ERROR", "unknown request type"); // !!!
              }
            }
          });
        } catch (e) {
          reject(e);
        }
      });
    } catch (e) {
      console.error("ERROR", "connection error", e);
      await asyncSleep(WEBSOCKET_RECONNECTION_TIMEOUT);
      await this.connect();
    }
  }

  async request(message) {
    if (
      !this.ws ||
      this.ws.readyState === WebSocket.CLOSING ||
      this.ws.readyState === WebSocket.CLOSED
    ) {
      await this.connect();
    } else if (this.ws.readyState === WebSocket.CONNECTING) {
      await new Promise((resolve, reject) => {
        this.deferredMessages.push({ resolve, reject });
      });
    }
    return new Promise((resolve, reject) => {
      const id = uuidv4(),
        type = "request";

      this.ws.send(JSON.stringify({ id, type, message }));
      this.awaitedMessages[id] = { resolve, reject };

      setTimeout(() => {
        reject("request timeout");
      }, WEBSOCKET_REQUEST_TIMEOUT);
    });
  }

  async notify(message) {
    if (
      !this.ws ||
      this.ws.readyState === WebSocket.CLOSING ||
      this.ws.readyState === WebSocket.CLOSED
    ) {
      await this.connect();
    } else if (this.ws.readyState === WebSocket.CONNECTING) {
      await new Promise((resolve, reject) => {
        this.deferredMessages.push({ resolve, reject });
      });
    }

    const id = uuidv4(),
      type = "notify";

    this.ws.send(JSON.stringify({ id, type, message }));
  }

  addNotificationListener(type, handler) {
    if (this.listeners.indexOf({ type, handler }) === -1) {
      this.listeners.push({ type, handler });
    }
  }

  removeNotificationListener(type, handler) {
    const i = this.listeners.indexOf({ type, handler });
    if (i > -1) {
      this.listeners.splice(i, 1);
    }
  }
}

export default Server;
