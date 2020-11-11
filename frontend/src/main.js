import Vue from "vue";
import Vuex from "vuex";
import VueRouter from "vue-router";
import Application from "./Application.vue";

import Store from "./store";

import Index from "./views/Index.vue";
import Desktop from "./views/Desktop.vue";
import Notes from "./views/Notes.vue";
import Categories from "./views/Categories.vue";
import Settings from "./views/Settings.vue";
import Account from "./views/Account.vue";
import Error from "./views/Error.vue";

Vue.use(Vuex);
Vue.use(VueRouter);

// Configs Vue behavior for prodution and developemnt modes
if (process.env.NODE_ENV === "production") {
  Vue.config.productionTip = false;
  Vue.config.devtools = false;
} else {
  Vue.config.productionTip = true;
  Vue.config.devtools = true;
}

// Creates Vue store instance
var store = new Vuex.Store(Store);

// Creates Vue router instance and configs routes of application
var router = new VueRouter({
  mode: "history",

  routes: [
    {
      path: "/",
      name: "index",
      component: Index,
      meta: {
        auth: false
      }
    },
    {
      path: "/app",
      component: Desktop,
      meta: {
        auth: true
      },
      children: [
        {
          path: "notes",
          name: "notes",
          component: Notes,
          meta: {
            auth: true
          }
        },
        {
          path: "categories",
          name: "categories",
          component: Categories,
          meta: {
            auth: true
          }
        },
        {
          path: "settings",
          name: "settings",
          component: Settings,
          meta: {
            auth: true
          }
        },
        {
          path: "account",
          name: "account",
          component: Account,
          meta: {
            auth: true
          }
        }
      ]
    },
    {
      path: "/error",
      name: "error",
      component: Error
    },
    {
      path: "*",
      redirect: "/error"
    }
  ]
});

// Setup watcher for user athorisation state maintance
store.watch(
  state => state.user,
  user => {
    if (user) {
      if (router.currentRoute.meta.auth === false) {
        router.push({ name: "notes" }).catch(() => {});
      }

      setTimeout(() => store.dispatch("loadModels"), 100);
    } else {
      if (router.currentRoute.meta.auth === true) {
        router.push({ name: "index" }).catch(() => {});
      }

      store.dispatch("clearState");
    }
  }
);

// Setup user authorisation validation when routing
router.beforeEach((to, from, next) => {
  var value = undefined;

  if (store.state.user) {
    if (to.meta.auth === false) {
      value = false;
    }
  } else if (!store.state.user) {
    if (to.meta.auth === true) {
      value = { name: "index" };
    }
  }
  next(value);
});

// Get user status from server
store.dispatch("status");

// Creates Vue instance and mount application
new Vue({
  router,
  store,
  render: h => h(Application)
}).$mount("#application");
