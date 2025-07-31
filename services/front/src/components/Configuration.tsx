import { type Component, createSignal } from "solid-js";
import { Settings } from "lucide-solid";

const Configuration: Component = () => {

  return (
    <div class="space-y-6">
      <div class="flex items-center gap-3">
        <Settings class="h-5 w-5" />
        <h2 class="text-2xl font-bold">Configuration</h2>
      </div>
    </div>
  );
};

export default Configuration;