import { Component, JSX, splitProps, createSignal, createEffect } from "solid-js";
import { cn } from "./utils";

interface SwitchProps extends Omit<JSX.ButtonHTMLAttributes<HTMLButtonElement>, 'onChange'> {
  checked?: boolean;
  defaultChecked?: boolean;
  onCheckedChange?: (checked: boolean) => void;
  disabled?: boolean;
}

const Switch: Component<SwitchProps> = (props) => {
  const [local, others] = splitProps(props, [
    "class", 
    "checked", 
    "defaultChecked", 
    "onCheckedChange", 
    "disabled",
    "onClick"
  ]);
  
  // Estado interno del switch
  const [internalChecked, setInternalChecked] = createSignal(
    local.checked ?? local.defaultChecked ?? false
  );
  
  // Determinar si el switch está controlado o no controlado
  const isControlled = () => local.checked !== undefined;
  const checkedValue = () => isControlled() ? local.checked! : internalChecked();
  
  // Sincronizar estado interno cuando cambia la prop checked
  createEffect(() => {
    if (isControlled()) {
      setInternalChecked(local.checked!);
    }
  });
  
  const handleClick = (event: MouseEvent & { currentTarget: HTMLButtonElement; target: Element; }) => {
    if (local.disabled) return;
    
    const newChecked = !checkedValue();
    
    // Si no está controlado, actualizar estado interno
    if (!isControlled()) {
      setInternalChecked(newChecked);
    }
    
    // Llamar callback si existe
    local.onCheckedChange?.(newChecked);
    
    // Llamar onClick original si existe
    if (typeof local.onClick === 'function') {
      local.onClick(event);
    }
  };
  
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checkedValue()}
      data-slot="switch"
      data-state={checkedValue() ? "checked" : "unchecked"}
      disabled={local.disabled}
      class={cn(
        "peer data-[state=checked]:bg-primary data-[state=unchecked]:bg-switch-background focus-visible:border-ring focus-visible:ring-ring/50 dark:data-[state=unchecked]:bg-input/80 inline-flex h-[1.15rem] w-8 shrink-0 items-center rounded-full border border-transparent transition-all outline-none focus-visible:ring-[3px] disabled:cursor-not-allowed disabled:opacity-50",
        local.class,
      )}
      onClick={handleClick}
      {...others}
    >
      <span
        data-slot="switch-thumb"
        class={cn(
          "bg-card dark:data-[state=unchecked]:bg-card-foreground dark:data-[state=checked]:bg-primary-foreground pointer-events-none block size-4 rounded-full ring-0 transition-transform data-[state=checked]:translate-x-[calc(100%-2px)] data-[state=unchecked]:translate-x-0",
        )}
        data-state={checkedValue() ? "checked" : "unchecked"}
      />
    </button>
  );
};

export { Switch };