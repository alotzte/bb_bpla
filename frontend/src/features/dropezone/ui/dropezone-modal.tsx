import { Modal } from 'antd';
import { useUnit } from 'effector-react';
import { $isOpen, dropezoneModalClosed, loadFiles } from '../model';
import { DropeZone } from '@/features/dropezone';
import { api } from '@/shared/services/api';
import { useState } from 'react';

interface DropezoneModalProps {
  type: api.FileType;
}

export const DropezoneModal = ({ type }: DropezoneModalProps) => {
  const [isOpen] = useUnit([$isOpen]);
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
        loadFiles(loadedFiles);
        setFiles([]);
        dropezoneModalClosed();
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
