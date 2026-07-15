interface Artifact {
  kind: string;
  path: string;
}

export function ArtifactViewer({ artifacts }: { artifacts: Artifact[] }) {
  if (artifacts.length === 0) return null;
  return (
    <div className="artifacts">
      <h4>Artifacts</h4>
      <ul>
        {artifacts.map((a) => (
          <li key={a.path}>
            <span className="kind">{a.kind}</span> {a.path}
          </li>
        ))}
      </ul>
    </div>
  );
}
