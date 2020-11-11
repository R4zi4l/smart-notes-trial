const ua = window.navigator.userAgent.toLowerCase();

const isIE = !!ua.match(/msie|trident\/7|edge/);
const isWinPhone = ua.indexOf("windows phone") !== -1;
const isIOS = !isWinPhone && !!ua.match(/ipad|iphone|ipod/);

const escapeHtml = string => {
  return string
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
};

const escapeRegExp = string => {
  return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
};

export default {
  isIE,
  isWinPhone,
  isIOS,
  escapeHtml,
  escapeRegExp
};
