export const dateToString = date => {
  const l2 = value => (value < 10 ? "0" + String(value) : String(value));
  const l3 = value => (value < 100 ? "0" + l2(value) : String(value));
  const l4 = value => (value < 1000 ? "0" + l3(value) : String(value));

  return `${l4(date.getFullYear())}-${l2(date.getMonth() + 1)}-${l2(
    date.getDate()
  )} ${l2(date.getHours())}:${l2(date.getMinutes())}:${l2(
    date.getSeconds()
  )}.${l3(date.getMilliseconds())}`;
};

export const asyncSleep = ms => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

export function makeDragAndDropMouseController(
  element,
  detail,
  beginDragHandler,
  processDragHandler,
  endDragHandler
) {
  var deltaX, deltaY, process;

  const mouserDownEventHandler = event => {
    process = false;

    deltaX = event.clientX - element.getBoundingClientRect().x;
    deltaY = event.clientY - element.getBoundingClientRect().y;

    window.addEventListener("mousemove", mouserDragEventHandler);
    window.addEventListener("mouseup", mouserUpEventHandler);
  };

  const mouserDragEventHandler = event => {
    event.preventDefault();
    event.stopPropagation();

    if (!process) {
      process = true;

      element.style.position = "fixed";
      element.style.zIndex = "10000";
      element.style.pointerEvents = "none";
      element.style.boxShadow = "0 0 0 1px $color-primary";

      beginDragHandler && beginDragHandler();
    }

    element.style.left = event.clientX - deltaX + "px";
    element.style.top = event.clientY - deltaY + "px";

    processDragHandler && processDragHandler();
  };

  const mouserUpEventHandler = event => {
    if (process) {
      event.preventDefault();
      event.stopPropagation();

      element.style = "";

      endDragHandler && endDragHandler();

      document
        .elementFromPoint(event.clientX, event.clientY)
        .dispatchEvent(new CustomEvent("drop", { detail, bubbles: true }));
    }

    window.removeEventListener("mousemove", mouserDragEventHandler);
    window.removeEventListener("mouseup", mouserUpEventHandler);
  };

  const c = {
    bind: () => {
      element.addEventListener("mousedown", mouserDownEventHandler);
    },

    unbind: () => {
      element.removeEventListener("mousedown", mouserDownEventHandler);
    }
  };

  return c;
}

// Touch events is musch more complecated and coupled all togather. Thougth to
// achive correct touch behaviour one needs to maintaine touch event globally.
export function makeDragAndDropTouchController(
  element,
  beginDragHandler,
  processDragHandler,
  endDragHandler
) {
  var lastX, lastY, process;

  const touchStartEventHandler = event => {
    lastX = event.touches[0].clientX;
    lastY = event.touches[0].clientY;
    process = false;

    window.addEventListener("touchmove", touchMoveEventHandler, {
      passive: false
    });
    window.addEventListener("touchend", touchEndEventHandler, {
      passive: false
    });
  };

  const touchMoveEventHandler = event => {
    event.preventDefault();

    if (!process) {
      process = true;
      beginDragHandler(lastX, lastY);
    }

    processDragHandler(
      (lastX = event.touches[0].clientX),
      (lastY = event.touches[0].clientY)
    );
  };

  const touchEndEventHandler = event => {
    if (process) {
      event.preventDefault();
      endDragHandler(lastX, lastY);
    }

    window.removeEventListener("touchmove", touchMoveEventHandler);
    window.removeEventListener("touchend", touchEndEventHandler);
  };

  const c = {
    bind: () => {
      element.addEventListener("touchstart", touchStartEventHandler, {
        passive: false
      });
    },

    unbind: () => {
      element.removeEventListener("touchstart", touchStartEventHandler);
    }
  };

  return c;
}
