const FileList = ({ files }) => {
    return (
      <div>
        <h2 className="filesHeader">Files</h2>
        <ol className="fileList">
          {files.map((file, index) => (
            <li key={index}>{file}</li>
          ))}
        </ol>
      </div>
    );
  };
  
  export default FileList;
  