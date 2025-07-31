import { type Component, createSignal } from "solid-js";
import { FileText } from "lucide-solid";
import FileUploader from "./FileUploader";

const FileSelection: Component = () => {
  const [sceneFile, setSceneFile] = createSignal<File | null>(null);
  const [ruleFile, setRuleFile] = createSignal<File | null>(null);

  // usar sceneFile() y ruleFile()

  return (
    <div class="space-y-6">
      <div class="flex items-center gap-3">
        <FileText class="h-5 w-5" />
        <h2 class="text-2xl font-bold">File Selection</h2>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <FileUploader
          title="Scene File"
          description="Select the XML file containing your simulation scene"
          onFileSelect={setSceneFile}
        />
        <FileUploader
          title="Rule File"
          description="Select the XML file containing your simulation rules"
          onFileSelect={setRuleFile}
        />
      </div>
    </div>
  );
};

export default FileSelection;