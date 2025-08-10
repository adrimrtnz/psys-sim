import { type Component, createSignal } from "solid-js";
import { MessageSquare } from "lucide-solid";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./Card";

const LogsPanel: Component = () => {

  return (
    <div class="space-y-6">
      <div class="flex items-center gap-3">
        <MessageSquare class="h-5 w-5" />
        <h2 class="text-2xl font-bold">Simulation Logs</h2>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Execution Log</CardTitle>
          <CardDescription>
            Real-time output from the simulation
          </CardDescription>
        </CardHeader>
      </Card>
    </div>
  )
}

export default LogsPanel;