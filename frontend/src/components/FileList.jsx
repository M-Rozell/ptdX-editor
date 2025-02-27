const FileList = ({ files }) => {
    return (
      <div>
        <h3>Files Found</h3>
        <ul>
          {files.map((file, index) => (
            <li key={index}>{file}</li>
          ))}
        </ul>
      </div>
    );
  };
  
  export default FileList;
  