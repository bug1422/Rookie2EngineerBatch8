import { useState, createContext, useEffect } from "react";
import { createRoot } from "react-dom/client";
import { ToastProps, Toast } from "./toast";
import { registerToastFn } from ".";

interface ToastItem extends ToastProps {
  id: string;
}

const ToastContext = createContext<(props: ToastProps) => void>(() => {});

export const ToastManager = () => {
  const [toasts, setToasts] = useState<ToastItem[]>([]);
  const MAX_VISIBLE_TOASTS = 3;

  const addToast = (props: ToastProps) => {
    const id = Math.random().toString(36).substring(2, 9);
    const item: ToastItem = { ...props, id };
    setToasts((prev) => [...prev, item]);
  };

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };
  useEffect(() => {
    registerToastFn(addToast);
  }, []);

  const visibleToasts = toasts.slice(-MAX_VISIBLE_TOASTS);
  return (
    <ToastContext.Provider value={addToast}>
      <div className="toast toast-top toast-center flex flex-col-reverse gap-y-2">
        {visibleToasts.map((t) => (
          <Toast key={t.id} {...t} onDismiss={() => removeToast(t.id)} />
        ))}
      </div>
    </ToastContext.Provider>
  );
};

// Initialize toast system
const initToastSystem = () => {
  const containerId = "toast-container";
  let container = document.getElementById(containerId);
  if (!container) {
    container = document.createElement("div");
    container.id = containerId;
    document.body.appendChild(container);
  }
  const root = createRoot(container);
  root.render(<ToastManager />);
};

initToastSystem();
