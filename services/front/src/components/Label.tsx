import { Component, JSX, splitProps } from "solid-js";
import { cn } from "./utils";

interface LabelProps extends JSX.LabelHTMLAttributes<HTMLLabelElement> {}

const Label: Component<LabelProps> = (props) => {
  const [local, others] = splitProps(props, ["class"]);
  
  return (
    <label
      data-slot="label"
      class={cn(
        "flex items-center gap-2 text-sm leading-none font-medium select-none group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50 peer-disabled:cursor-not-allowed peer-disabled:opacity-50",
        local.class,
      )}
      {...others}
    />
  );
};

export { Label };