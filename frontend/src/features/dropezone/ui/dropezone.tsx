import { api } from '@/shared/services/api';
import Dropzone from 'react-dropzone';

interface DropeZoneProps {
  onDrop: (files: File[]) => void;
  type: api.FileType;
}

const imageAccept = {
  'image/apng': [],
  'image/avif': [],
  'image/bmp': [],
  'image/jpeg': [],
  'image/jpg': [],
  'image/png': [],
  'image/tif': [],
  'image/tiff': [],
  'image/webp': [],
};

const videoAccept = {
  'video/avi': [],
  'video/mp4': [],
  'video/mpeg': [],
  'video/ogv': [],
  'video/webm': [],
};

export const DropeZone = ({ onDrop, type }: DropeZoneProps) => {
  return (
    <Dropzone
      onDrop={(files) => onDrop(files)}
      multiple={type === 'image'}
      accept={type === 'image' ? imageAccept : videoAccept}
    >
      {({ getRootProps, getInputProps }) => (
        <div {...getRootProps()}>
          <input {...getInputProps()} />
          <div style={style.drope}>
            <div>Перетащите сюда файлы или нажмите и выберите нужные</div>
          </div>
        </div>
      )}
    </Dropzone>
  );
};

const style = {
  drope: {
    width: '360px',
    height: '160px',
    backgroundColor: '#f0f0f0',
    border: '2px #c8c8c8 dashed',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    padding: '16px',
    textAlign: 'center' as const,
    color: '#505050',
    marginTop: '24px',
    cursor: 'pointer',
  },
};
