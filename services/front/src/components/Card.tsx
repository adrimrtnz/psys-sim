import { Component, JSX, splitProps } from "solid-js";
import { cn } from "./utils";

interface CardProps extends JSX.HTMLAttributes<HTMLDivElement> {}

const Card: Component<CardProps> = (props) => {
  const [local, others] = splitProps(props, ["class"]);

  return (
    <div
      data-slot="card"
      class={cn(
        "bg-card text-card-foreground flex flex-col gap-6 rounded-xl border",
        local.class,
      )}
      {...others}
    />
  );
};

const CardHeader: Component<CardProps> = (props) => {
  const [local, others] = splitProps(props, ["class"]);
  
  return (
    <div
      data-slot="card-header"
      class={cn(
        "@container/card-header grid auto-rows-min grid-rows-[auto_auto] items-start gap-1.5 px-6 pt-6 has-data-[slot=card-action]:grid-cols-[1fr_auto] [.border-b]:pb-6",
        local.class,
      )}
      {...others}
    />
  );
};

const CardTitle: Component<CardProps> = (props) => {
  const [local, others] = splitProps(props, ["class"]);
  
  return (
    <h4
      data-slot="card-title"
      class={cn("leading-none", local.class)}
      {...others}
    />
  );
};

const CardDescription: Component<CardProps> = (props) => {
  const [local, others] = splitProps(props, ["class"]);
  
  return (
    <p
      data-slot="card-description"
      class={cn("text-muted-foreground", local.class)}
      {...others}
    />
  );
};

const CardAction: Component<CardProps> = (props) => {
  const [local, others] = splitProps(props, ["class"]);
  
  return (
    <div
      data-slot="card-action"
      class={cn(
        "col-start-2 row-span-2 row-start-1 self-start justify-self-end",
        local.class,
      )}
      {...others}
    />
  );
};

const CardContent: Component<CardProps> = (props) => {
  const [local, others] = splitProps(props, ["class"]);
  
  return (
    <div
      data-slot="card-content"
      class={cn("px-6 [&:last-child]:pb-6", local.class)}
      {...others}
    />
  );
};

const CardFooter: Component<CardProps> = (props) => {
  const [local, others] = splitProps(props, ["class"]);
  
  return (
    <div
      data-slot="card-footer"
      class={cn("flex items-center px-6 pb-6 [.border-t]:pt-6", local.class)}
      {...others}
    />
  );
};

export {
  Card,
  CardHeader,
  CardFooter,
  CardTitle,
  CardAction,
  CardDescription,
  CardContent,
};
