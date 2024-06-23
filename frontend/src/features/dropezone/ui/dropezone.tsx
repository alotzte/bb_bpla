import { api } from '@/shared/services/api';
import { LoadingOutlined } from '@ant-design/icons';
import { Flex, Spin, Typography } from 'antd';
import Dropzone from 'react-dropzone';

const { Title } = Typography;

interface DropeZoneProps {
  onDrop: (files: File[]) => void;
  type: api.FileType;
  fileNames: string[];
  isLoading: boolean;
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

const archiveAccept = {
  'application/zip': [],
};

const typesAccept: Record<api.FileType, { [key: string]: string[] }> = {
  archive: archiveAccept,
  image: imageAccept,
  video: videoAccept,
};

export const DropeZone = ({
  onDrop,
  type,
  fileNames,
  isLoading,
}: DropeZoneProps) => {
  return (
    <Dropzone
      onDrop={(files) => onDrop(files)}
      multiple={type === 'image'}
      accept={typesAccept[type]}
    >
      {({ getRootProps, getInputProps }) => (
        <div {...getRootProps()}>
          <input {...getInputProps()} />
          <div style={style.drope}>
            {isLoading ? (
              <Flex vertical gap="small">
                <Title level={3}>Загружаем файлы</Title>
                <Spin size="large" indicator={<LoadingOutlined spin />} />
              </Flex>
            ) : fileNames.length ? (
              <Flex vertical>
                {fileNames.map((filename, index) => (
                  <div key={index}>{filename}</div>
                ))}
              </Flex>
            ) : (
              <div>Перетащите сюда файлы или нажмите и выберите нужные</div>
            )}
          </div>
        </div>
      )}
    </Dropzone>
  );
};

const style = {
  drope: {
    width: '360px',
    minHeight: '160px',
    backgroundColor: '#f0f0f0',
    border: '2px #c8c8c8 dashed',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    padding: '16px',
    textAlign: 'center' as const,
    color: '#505050',
    margin: '32px 0 8px',
    cursor: 'pointer',
  },
};
