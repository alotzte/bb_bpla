import { useUnit } from 'effector-react';
import {
  $isOpen,
  $selectedId,
  fileModalClosed,
  resetSelectedId,
} from '../model';
import { Flex, Modal, Result } from 'antd';
import { useEffect } from 'react';
import { fileInfoModel } from '@/entities/files';
import { Player } from './player';
import styled from 'styled-components';

export const FileModal = () => {
  const [isOpen] = useUnit([$isOpen]);

  const [selectedId, isLoading, file, notFound] = useUnit([
    $selectedId,
    fileInfoModel.$isLoading,
    fileInfoModel.$item,
    fileInfoModel.$notFound,
  ]);

  useEffect(() => {
    if (selectedId) {
      fileInfoModel.getItemFx(selectedId);
    }
  }, [selectedId]);

  return (
    <Modal
      open={isOpen}
      onCancel={() => {
        resetSelectedId();
        fileModalClosed();
      }}
      footer={null}
      width={760}
      closeIcon={null}
      loading={isLoading}
    >
      <Flex justify="center" align="center">
        {notFound && (
          <Result
            title="Не удалось загрузить информацию"
            subTitle="Попробуйте повторить запрос чуть позже"
          />
        )}
        {file &&
          (file?.type === 'video' ? (
            <Player file={file} />
          ) : (
            <Image src={file?.link} />
          ))}
      </Flex>
    </Modal>
  );
};

const Image = styled.img`
  max-width: 720px;
`;
