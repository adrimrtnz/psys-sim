import { type Component, createSignal } from "solid-js";
import { Settings } from "lucide-solid";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./Card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./Select"
import { Label } from "./Label";
import { Input } from "./Input"


export interface SimulatorConfig {
  derivationMode: string;
  timesteps: number;
  updateInterval: number;
  enableLogging: boolean;
  randomSeed: string;
}

interface ConfigurationPanelProps {
  config: SimulatorConfig,
  onConfigChange: (config: SimulatorConfig) => void
}

const ConfigurationPanel: Component<ConfigurationPanelProps> = (props) => {
  const updateConfig = (field: keyof SimulatorConfig, value: any) => {
    props.onConfigChange({
      ...props.config,
      [field]: value,
    });
  };

  return (
    <div class="space-y-6">
      <div class="flex items-center gap-3">
        <Settings class="h-5 w-5" />
        <h2 class="text-2xl font-bold">Configuration</h2>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Simulation Configuration</CardTitle>
          <CardDescription>
            Configure the parameters
          </CardDescription>
        </CardHeader>

        <CardContent class="space-y-6">

          <div class="space-y-2">
            <Label for="derivationMode">Derivation Mode</Label>
            <Select
              value={props.config.derivationMode}
              onValueChange={(value) => updateConfig('derivationMode', value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select the derivation mode" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="minpar">Min. parallelism</SelectItem>
                  <SelectItem value="maxpar">Max. parallelism</SelectItem>
                </SelectContent>
              </Select>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-2">
              <Label for="timesteps">Computation Steps</Label>
              <Input
                id="timesteps"
                type="number"
                value={props.config.timesteps}
                onInput={(e) => updateConfig('timesteps', parseInt(e.currentTarget.value) || 0)}
                min="0"
                max="10000"
              />
            </div>

            <div class="space-y-2">
              <Label for="updateInterval">Update Interval</Label>
              <Input
                id="updateInterval"
                type="number"
                value={props.config.updateInterval}
                onInput={(e) => updateConfig('updateInterval', parseInt(e.currentTarget.value) || 0)}
                min="1"
                max="5000"
              />
            </div>
          </div>

        </CardContent>

      </Card>
    </div>
  );
};

export default ConfigurationPanel;