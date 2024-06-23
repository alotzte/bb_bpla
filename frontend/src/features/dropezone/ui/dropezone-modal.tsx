import { Modal } from 'antd';
import { useUnit } from 'effector-react';
import {
  $isOpen,
  $isUploading,
  dropezoneModalClosed,
  loadFiles,
  loadSingleFile,
} from '../model';
import { DropeZone } from '@/features/dropezone';
import { api } from '@/shared/services/api';
import { useState } from 'react';

interface DropezoneModalProps {
  type: api.FileType;
}

export const DropezoneModal = ({ type }: DropezoneModalProps) => {
  const [isOpen, isLoading] = useUnit([$isOpen, $isUploading]);
  const [loadedFiles, setFiles] = useState<File[]>([]);

  const onDrop = (files: File[]) => {
    const filteredFiles = files.filter(
      (file) => !loadedFiles.map((s) => s.name).includes(file.name)
    );
    setFiles([...loadedFiles, ...filteredFiles]);
  };

  return (
    <Modal
      open={isOpen}
      onOk={() => {
        if (type === 'image') {
          loadFiles(loadedFiles);
        } else {
          loadSingleFile(loadedFiles[0]);
        }
        setFiles([]);
      }}
      onCancel={() => {
        dropezoneModalClosed();
        setFiles([]);
      }}
      style={style.modal}
    >
      <DropeZone
        onDrop={onDrop}
        type={type}
        fileNames={loadedFiles.map((file) => file.name)}
        isLoading={isLoading}
      />
    </Modal>
  );
};

const style = {
  modal: {
    display: 'flex',
    width: '100%',
    paddingTop: '24px',
    justifyContent: 'center',
  },
};
