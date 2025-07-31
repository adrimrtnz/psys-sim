import type { Component } from 'solid-js';
import { Separator } from '@kobalte/core/separator';
import FileSelection from './components/FileSelection';
import Configuration from './components/Configuration'

const App: Component = () => {
  return (
    <div class="min-h-screen bg-background p-6">
      <div class="max-w-7xl mx-auto space-y-6">
        <div class="space-y-2">
          <h1 class="text-3xl font-bold">P System Simulator</h1>
          <p class="text-muted-foreground">Configure and run the simulation with XML scene and rule files</p>
        </div>

      <Separator class="separator"/>

      <FileSelection />

      <Separator class="separator" />

      <Configuration />

      </div>
    </div>
  );
};

export default App;
