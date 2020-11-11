import { dateToString } from "./../utils/utils.js";

export const decodeModels = response => {
  let note = {},
    category = {},
    categoryentity = {};

  for (let key in response.note) {
    let value = response.note[key];
    note[key] = decodeModelItem("note", key, {
      updated: value[1],
      title: value[2],
      text: value[3]
    });
  }

  for (let key in response.category) {
    let value = response.category[key];
    category[key] = decodeModelItem("category", key, {
      updated: value[1],
      title: value[2],
      text: value[3],
      parent: value[4]
    });
  }

  for (let key in response.categoryentity) {
    let value = response.categoryentity[key];
    categoryentity[key] = decodeModelItem("categoryentity", key, {
      updated: value[2]
    });
  }

  return {
    note,
    category,
    categoryentity
  };
};

export const decodeModelItem = (model, id, item = {}) => {
  if (model === "note") {
    return {
      id: id || "",
      updated: item.updated ? new Date(item.updated) : new Date(),
      title: item.title || "",
      text: item.text || ""
    };
  } else if (model === "category") {
    return {
      id: id || "",
      updated: item.updated ? new Date(item.updated) : new Date(),
      title: item.title || "",
      text: item.text || "",
      parent: item.parent || undefined
    };
  } else if (model === "categoryentity") {
    return {
      category: getCategoryFromCategoryEntityId(id || ""),
      entity: getEntityFromCategoryEntityId(id || ""),
      updated: item.updated ? new Date(item.updated) : new Date()
    };
  }
  return {};
};

export const encodeModelItem = (model, item) => {
  model;
  if (item.updated) {
    item.updated = dateToString(item.updated);
  }
  return item;
};

export const getEntityFromCategoryEntityId = id => {
  return id.slice(id.length - 36);
};

export const getCategoryFromCategoryEntityId = id => {
  return id.slice(0, 36);
};

export const makeCategoryEntityId = (category, entity) => {
  return category + entity;
};
