import { ToastProps } from "./toast";
import "./ToastManager"
let toastFn: ((props: ToastProps) => void) | null = null;

export const registerToastFn = (fn: (props: ToastProps) => void) => {
  toastFn = fn;
};

export default function toast(props: ToastProps) {
  if (toastFn) {
    toastFn(props);
  } else {
    console.warn("Toast system not initialized");
  }
}
