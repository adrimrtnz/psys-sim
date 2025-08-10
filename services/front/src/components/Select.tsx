import { Component, JSX, splitProps, createSignal, createEffect, children, Show, For, createContext, useContext } from "solid-js";
import { Portal } from "solid-js/web";
import { CheckIcon, ChevronDownIcon, ChevronUpIcon } from "lucide-solid";
import { cn } from "./utils";

// Context para pasar datos entre componentes del Select
interface SelectContextValue {
  value: () => string;
  onValueChange: (value: string) => void;
  open: () => boolean;
  setOpen: (open: boolean) => void;
  placeholder?: string;
}

const SelectContext = createContext<SelectContextValue>();

interface SelectProps {
  value?: string;
  defaultValue?: string;
  onValueChange?: (value: string) => void;
  children?: JSX.Element;
  disabled?: boolean;
}

const Select: Component<SelectProps> = (props) => {
  const [local, others] = splitProps(props, ["value", "defaultValue", "onValueChange", "children", "disabled"]);
  
  const [internalValue, setInternalValue] = createSignal(local.value ?? local.defaultValue ?? "");
  const [open, setOpen] = createSignal(false);
  
  // Determinar si está controlado
  const isControlled = () => local.value !== undefined;
  const currentValue = () => isControlled() ? local.value! : internalValue();
  
  // Sincronizar estado interno
  createEffect(() => {
    if (isControlled() && local.value !== undefined) {
      setInternalValue(local.value);
    }
  });
  
  const handleValueChange = (newValue: string) => {
    if (!isControlled()) {
      setInternalValue(newValue);
    }
    local.onValueChange?.(newValue);
    setOpen(false);
  };
  
  const contextValue: SelectContextValue = {
    value: currentValue,
    onValueChange: handleValueChange,
    open,
    setOpen,
  };
  
  return (
    <SelectContext.Provider value={contextValue}>
      <div data-slot="select" {...others}>
        {local.children}
      </div>
    </SelectContext.Provider>
  );
};

interface SelectTriggerProps extends JSX.ButtonHTMLAttributes<HTMLButtonElement> {
  size?: "sm" | "default";
}

const SelectTrigger: Component<SelectTriggerProps> = (props) => {
  const [local, others] = splitProps(props, ["class", "size", "children"]);
  const context = useContext(SelectContext);
  if (!context) throw new Error("SelectTrigger must be used within Select");
  
  let triggerRef: HTMLButtonElement | undefined;

  const handleClick = (e: MouseEvent) => {
    e.stopPropagation()
    context.setOpen(!context.open());
    const currentState = context.open();
    console.log("SelectTrigger clicked, current open state:", currentState);
    console.log("Setting open to:", !currentState);

    // Posicionar el dropdown
    if (triggerRef && !currentState) {
      const rect = triggerRef.getBoundingClientRect();
      console.log("Trigger position:", rect);
      
      // Guardar posición en el contexto (necesitaremos expandir la interface)
      setTimeout(() => {
        const dropdown = document.querySelector('[data-slot="select-content"]') as HTMLElement;
        if (dropdown) {
          dropdown.style.position = 'fixed';
          dropdown.style.top = `${rect.bottom + window.scrollY}px`;
          dropdown.style.left = `${rect.left + window.scrollX}px`;
          dropdown.style.minWidth = `${rect.width}px`;
          console.log("Dropdown positioned at:", dropdown.style.top, dropdown.style.left);
        }
      }, 0);
    }
  };
  
  return (
    <button
      ref={triggerRef}
      type="button"
      data-slot="select-trigger"
      data-size={local.size || "default"}
      class={cn(
        "border-input data-[placeholder]:text-muted-foreground [&_svg:not([class*='text-'])]:text-muted-foreground focus-visible:border-ring focus-visible:ring-ring/50 aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive dark:bg-input/30 dark:hover:bg-input/50 flex w-full items-center justify-between gap-2 rounded-md border bg-input-background px-3 py-2 text-sm whitespace-nowrap transition-[color,box-shadow] outline-none focus-visible:ring-[3px] disabled:cursor-not-allowed disabled:opacity-50 data-[size=default]:h-9 data-[size=sm]:h-8 *:data-[slot=select-value]:line-clamp-1 *:data-[slot=select-value]:flex *:data-[slot=select-value]:items-center *:data-[slot=select-value]:gap-2 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4",
        local.class,
      )}
      onClick={handleClick}
      {...others}
    >
      {local.children}
      <ChevronDownIcon class="size-4 opacity-50" />
    </button>
  );
};

interface SelectValueProps extends JSX.HTMLAttributes<HTMLSpanElement> {
  placeholder?: string;
}

const SelectValue: Component<SelectValueProps> = (props) => {
  const [local, others] = splitProps(props, ["class", "placeholder"]);
  const context = useContext(SelectContext);
  if (!context) throw new Error("SelectValue must be used within Select");
  
  return (
    <span
      data-slot="select-value"
      class={cn("line-clamp-1 flex items-center gap-2", local.class)}
      {...others}
    >
      <Show when={context.value()} fallback={local.placeholder}>
        {context.value()}
      </Show>
    </span>
  );
};

interface SelectContentProps extends JSX.HTMLAttributes<HTMLDivElement> {
  position?: "popper";
}

const SelectContent: Component<SelectContentProps> = (props) => {
  const [local, others] = splitProps(props, ["class", "children", "position"]);
  const context = useContext(SelectContext);
  if (!context) throw new Error("SelectContent must be used within Select");
  
  let contentRef: HTMLDivElement | undefined;
  
  // Cerrar cuando se hace click fuera
  const handleOutsideClick = (e: Event) => {
    if (contentRef && !contentRef.contains(e.target as Node)) {
      context.setOpen(false);
    }
  };
  
  createEffect(() => {
    if (context.open()) {
      document.addEventListener('click', handleOutsideClick);
      return () => document.removeEventListener('click', handleOutsideClick);
    }
  });
  
  return (
    <Show when={context.open()}>
      <Portal>
        <div
          ref={contentRef}
          data-slot="select-content"
          class={cn(
            "bg-popover text-popover-foreground relative z-50 max-h-96 min-w-[8rem] overflow-x-hidden overflow-y-auto rounded-md border shadow-md animate-in fade-in-0 zoom-in-95 slide-in-from-top-2",
            local.position === "popper" && "translate-y-1",
            local.class,
          )}
          {...others}
        >
          <div class="p-1">
            {local.children}
          </div>
        </div>
      </Portal>
    </Show>
  );
};

interface SelectItemProps extends JSX.HTMLAttributes<HTMLDivElement> {
  value: string;
}

const SelectItem: Component<SelectItemProps> = (props) => {
  const [local, others] = splitProps(props, ["class", "children", "value"]);
  const context = useContext(SelectContext);
  if (!context) throw new Error("SelectItem must be used within Select");
  
  const handleClick = () => {
    context.onValueChange(local.value);
  };
  
  const isSelected = () => context.value() === local.value;
  
  return (
    <div
      data-slot="select-item"
      class={cn(
        "focus:bg-accent focus:text-accent-foreground [&_svg:not([class*='text-'])]:text-muted-foreground relative flex w-full cursor-default items-center gap-2 rounded-sm py-1.5 pr-8 pl-2 text-sm outline-hidden select-none data-[disabled]:pointer-events-none data-[disabled]:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4 hover:bg-accent hover:text-accent-foreground",
        local.class,
      )}
      onClick={handleClick}
      {...others}
    >
      <Show when={isSelected()}>
        <span class="absolute right-2 flex size-3.5 items-center justify-center">
          <CheckIcon class="size-4" />
        </span>
      </Show>
      <span>{local.children}</span>
    </div>
  );
};

const SelectGroup: Component<JSX.HTMLAttributes<HTMLDivElement>> = (props) => {
  const [local, others] = splitProps(props, ["class"]);
  
  return (
    <div
      data-slot="select-group"
      class={local.class}
      {...others}
    />
  );
};

const SelectLabel: Component<JSX.HTMLAttributes<HTMLDivElement>> = (props) => {
  const [local, others] = splitProps(props, ["class"]);
  
  return (
    <div
      data-slot="select-label"
      class={cn("text-muted-foreground px-2 py-1.5 text-xs", local.class)}
      {...others}
    />
  );
};

const SelectSeparator: Component<JSX.HTMLAttributes<HTMLDivElement>> = (props) => {
  const [local, others] = splitProps(props, ["class"]);
  
  return (
    <div
      data-slot="select-separator"
      class={cn("bg-border pointer-events-none -mx-1 my-1 h-px", local.class)}
      {...others}
    />
  );
};

// Componentes simplificados para scroll buttons (no funcionales en esta implementación básica)
const SelectScrollUpButton: Component<JSX.HTMLAttributes<HTMLDivElement>> = (props) => {
  const [local, others] = splitProps(props, ["class"]);
  
  return (
    <div
      data-slot="select-scroll-up-button"
      class={cn("flex cursor-default items-center justify-center py-1", local.class)}
      {...others}
    >
      <ChevronUpIcon class="size-4" />
    </div>
  );
};

const SelectScrollDownButton: Component<JSX.HTMLAttributes<HTMLDivElement>> = (props) => {
  const [local, others] = splitProps(props, ["class"]);
  
  return (
    <div
      data-slot="select-scroll-down-button"
      class={cn("flex cursor-default items-center justify-center py-1", local.class)}
      {...others}
    >
      <ChevronDownIcon class="size-4" />
    </div>
  );
};

export {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectScrollDownButton,
  SelectScrollUpButton,
  SelectSeparator,
  SelectTrigger,
  SelectValue,
};