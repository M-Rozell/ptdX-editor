
const FileList = ({ files }) => {
    return (
      <div>       
        <ol className="fileList">
          {files.map((file, index) => (
            <li key={index}>{file}</li>
          ))}
        </ol>
      </div>
    );
  };
  
  export default FileList;
  