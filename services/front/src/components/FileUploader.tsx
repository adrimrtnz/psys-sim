import { type Component, createSignal, Show } from "solid-js";
import { Upload, X } from "lucide-solid";
import { cn } from "./utils"; // La función que creamos antes

type FileUploaderProps = {
  title: string;
  description: string;
  onFileSelect: (file: File | null) => void;
};

const FileUploader: Component<FileUploaderProps> = (props) => {
  const [selectedFile, setSelectedFile] = createSignal<File | null>(null);
  const [isDragging, setIsDragging] = createSignal(false);
  let fileInputRef!: HTMLInputElement;

  const handleFileChange = (files: FileList | null) => {
    const file = files?.[0];
    if (file && file.type === "text/xml") {
      setSelectedFile(file);
      props.onFileSelect(file);
    } else {
      alert("Please select a valid .xml file.");
    }
  };

  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    handleFileChange(e.dataTransfer?.files ?? null);
  };
  
  const clearFile = () => {
    setSelectedFile(null);
    props.onFileSelect(null);
    fileInputRef.value = ""; // Resetea el input
  };

  return (
    <div class="bg-card p-6 rounded-lg border text-card-foreground shadow-sm w-full">
      <div class="space-y-1.5 mb-4">
        <h3 class="font-semibold tracking-tight text-lg">{props.title}</h3>
        <p class="text-sm text-muted-foreground">{props.description}</p>
      </div>

      <Show
        when={selectedFile()}
        fallback={
          <div
            class={cn(
              "flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-md transition-colors",
              isDragging() ? "border-primary bg-accent" : "border-border"
            )}
            onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={handleDrop}
          >
            <input
              ref={fileInputRef}
              type="file"
              class="hidden"
              accept=".xml"
              onChange={(e) => handleFileChange(e.currentTarget.files)}
            />
            <Upload class="w-8 h-8 text-muted-foreground mb-2" />
            <p class="text-sm text-muted-foreground">
              Drop your .xml file here, or
            </p>
            <button
              onClick={() => fileInputRef.click()}
              class="mt-2 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2 rounded-md text-sm font-medium"
            >
              Choose File
            </button>
          </div>
        }
      >
        {/* Vista cuando ya hay un archivo seleccionado */}
        <div class="flex items-center justify-between p-4 bg-muted rounded-md border">
          <p class="text-sm font-medium truncate">{selectedFile()!.name}</p>
          <button onClick={clearFile} class="p-1 text-muted-foreground hover:text-destructive">
            <X class="w-5 h-5" />
          </button>
        </div>
      </Show>
    </div>
  );
};

export default FileUploader;