import { useState } from "react";

interface Props {
  disabled: boolean;
  onSubmit: (description: string) => void;
}

export function TaskComposer({ disabled, onSubmit }: Props) {
  const [text, setText] = useState("");
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (text.trim()) onSubmit(text.trim());
      }}
    >
      <textarea
        value={text}
        disabled={disabled}
        placeholder="Describe the task for the agents…"
        onChange={(e) => setText(e.target.value)}
      />
      <button type="submit" disabled={disabled || !text.trim()}>
        Start run
      </button>
    </form>
  );
}
