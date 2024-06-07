import { Modal } from 'antd';
import { useUnit } from 'effector-react';
import { $isOpen, dropezoneModalClosed, loadFilesFx } from '../model';
import { DropeZone } from '@/features/dropezone';
import { api } from '@/shared/services/api';

interface DropezoneModalProps {
  type: api.FileType;
}

export const DropezoneModal = ({ type }: DropezoneModalProps) => {
  const [isOpen] = useUnit([$isOpen]);

  const onDrop = (files: File[]) => {
    loadFilesFx(files);
    dropezoneModalClosed();
  };

  return (
    <Modal
      open={isOpen}
      onOk={() => dropezoneModalClosed()}
      onCancel={() => dropezoneModalClosed()}
      style={style.modal}
    >
      <DropeZone onDrop={onDrop} type={type} />
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
