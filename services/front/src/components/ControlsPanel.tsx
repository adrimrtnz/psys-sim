import { type Component, createSignal } from "solid-js";
import { Play } from "lucide-solid";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./Card";

const ControlsPanel: Component = () => {

  return (
    <div class="space-y-6">
      <div class="flex items-center gap-3">
        <Play class="h-5 w-5" />
        <h2 class="text-2xl font-bold">Simulation Controls</h2>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Simulation Controls</CardTitle>
          <CardDescription>
            Run the simulation end-to-end or step-by-step
          </CardDescription>
        </CardHeader>
      </Card>
    </div>
  )
}

export default ControlsPanel;