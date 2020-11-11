import Vue from "vue";
import Server from "./server.js";
import { v4 as uuidv4 } from "uuid";
import { decodeModels, decodeModelItem, encodeModelItem } from "./model.js";
import { dateToString } from "./../utils/utils.js";

const TRANSACTION_DELAY = 5000;

var server = new Server();

// Transactions structure:
// [
//   {
//     id: uuuid,                                 // transaction id
//     status: created | sent | declined | done,  // transaction status
//     timer: Timer                               // transaction timer identifier
//     items: [
//       {
//         model,     // model name = string
//         id,        // client's item id
//         updated,   // item last update = datetime
//         status,    // operation status = insert | update | delete | erase
//         item       // item data = { updated, ... }
//       }
//     ]
//   }
// ]
const makeTransaktion = () => {
  return {
    id: uuidv4(),
    status: "created",
    timer: undefined,
    items: [],
    prepared: []
  };
};

var transactions = [makeTransaktion()];

// Store initialization plugin
const init = store => {
  server.addNotificationListener("update_models_items", message =>
    store.dispatch("updateModels", message)
  );
};

export default {
  plugins: [init],

  state: {
    user: undefined,

    note: {},
    category: {},
    categoryentity: {}
  },

  getters: {
    newId: () => {
      return () => uuidv4();
    }
  },

  mutations: {
    clearState: state => {
      Vue.set(state, "user", undefined);

      Vue.set(state, "note", {});
      Vue.set(state, "category", {});
      Vue.set(state, "categoryentity", {});
    },

    setUser: (state, user) => {
      Vue.set(state, "user", user);
    },

    setModel: (state, { model, data }) => {
      Vue.set(state, model, data);
    },

    setModelItem: (state, { model, id, item }) => {
      Vue.set(state[model], id, Object.assign(state[model][id] || {}, item));
    },

    deleteModelItem: (state, { model, id }) => {
      Vue.delete(state[model], id);
    }
  },

  actions: {
    clearState: async ({ commit }) => {
      transactions = [makeTransaktion()];
      commit("clearState");
    },

    status: async ({ commit }) => {
      const response = await server.request({
        type: "status"
      });

      if (response.status === "ok") {
        if (response.session) {
          commit("setUser", {
            username: response.username
          });
        } else {
          commit("setUser", undefined);
        }
        document.cookie =
          "session=" +
          response.session +
          ";expires=" +
          new Date(Date.now() + 604800000).toUTCString();
      } else {
        throw response;
      }
    },

    login: async ({ commit }, { email, password }) => {
      const response = await server.request({
        type: "login",
        email,
        password
      });

      if (response.status === "ok") {
        commit("setUser", {
          username: response.username
        });
        document.cookie =
          "session=" +
          response.session +
          ";expires=" +
          new Date(Date.now() + 604800000).toUTCString();
      } else {
        throw response;
      }
    },

    register: async ({ commit }, { username, email, password }) => {
      const response = await server.request({
        type: "register",
        username,
        email,
        password
      });

      if (response.status === "ok") {
        commit("setUser", {
          username: response.username
        });
        document.cookie =
          "session=" +
          response.session +
          ";expires=" +
          new Date(Date.now() + 604800000).toUTCString();
      } else {
        throw response;
      }
    },

    logout: async () => {},

    loadModels: async ({ commit }) => {
      const response = await server.request({
        type: "load_models"
      });

      if (response.status === "ok") {
        const models = decodeModels(response);

        for (let model in models) {
          commit("setModel", { model, data: models[model] });
        }
      } else {
        throw response;
      }
    },

    updateModels: async ({ commit }, { accepted }) => {
      for (let item of accepted) {
        console.log("UPDATE MODELS", item);
        if (item.status === "insert") {
          commit("setModelItem", {
            model: item.model,
            id: item.id,
            item: decodeModelItem(item.model, item.id, item.item)
          });
        } else if (item.status === "update") {
          commit("setModelItem", {
            model: item.model,
            id: item.id,
            item: item.item
          });
        } else if (item.status === "delete") {
          commit("deleteModelItem", {
            model: item.model,
            id: item.id
          });
        }
      }
    },

    setModelItem: async ({ state, commit, dispatch }, { model, id, item }) => {
      var updated, status;

      if (state[model][id]) {
        updated = state[model][id].updated;
        item.updated = new Date();
        status = "update";
      } else {
        item = decodeModelItem(model, id, item);
        item.updated = updated = new Date();
        status = "insert";
      }

      commit("setModelItem", { model, id, item });

      transactions[transactions.length - 1].items.push({
        model,
        id,
        updated,
        status,
        item
      });

      clearTimeout(transactions[transactions.length - 1].timer);
      transactions[transactions.length - 1].timer = setTimeout(
        () => dispatch("sendTransactions"),
        TRANSACTION_DELAY
      );
    },

    deleteModelItem: async ({ state, commit, dispatch }, { model, id }) => {
      if (!state[model][id]) {
        return;
      }

      var updated = state[model][id].updated,
        status = "delete";

      commit("deleteModelItem", { model, id });

      transactions[transactions.length - 1].items.push({
        model,
        id,
        updated,
        status,
        item: {}
      });

      clearTimeout(transactions[transactions.length - 1].timer);
      transactions[transactions.length - 1].timer = setTimeout(
        () => dispatch("sendTransactions"),
        TRANSACTION_DELAY
      );
    },

    sendTransactions: async () => {
      var transaction = transactions[transactions.length - 1];
      transactions.push(makeTransaktion());

      for (let item of transaction.items) {
        let prepared = transaction.prepared.find(
          element => element.model === item.model && element.id === item.id
        );

        if (!prepared) {
          transaction.prepared.push({ ...item });
        } else {
          if (item.status === "update") {
            if (prepared.status !== "delete") {
              prepared.item = {
                ...prepared.item,
                ...item.item
              };
            }
          } else if (item.status === "delete" && prepared.status === "insert") {
            transaction.prepared.splice(
              transaction.prepared.indexOf(prepared),
              1
            );
          } else {
            prepared.status = item.status;
            prepared.item = item.item;
          }
        }
      }

      for (let item of transaction.prepared) {
        if (item.updated) {
          item.updated = dateToString(item.updated);
        }
        item.item = encodeModelItem(item.model, item.item);
      }

      transaction.state = "sent";

      const response = await server.request({
        type: "update_models_items",
        id: transaction.id,
        items: transaction.prepared
      });

      if (response.status === "ok") {
        console.log("sendTransactions", "EVERYTHIN IS OK", response);
      } else {
        throw response;
      }
    }
  }
};
