interface Props {
  projects: { id: string; name: string }[];
  value: string;
  onChange: (id: string) => void;
}

export function ProjectPicker({ projects, value, onChange }: Props) {
  return (
    <select value={value} onChange={(e) => onChange(e.target.value)}>
      <option value="">Select a project…</option>
      {projects.map((p) => (
        <option key={p.id} value={p.id}>
          {p.name}
        </option>
      ))}
    </select>
  );
}
