import { api } from '@/shared/services/api';
import { ConfigProvider, Flex, Slider } from 'antd';
import { useRef, useState } from 'react';
import ReactPlayer from 'react-player';
import styled from 'styled-components';
import Play from '@/assets/triangle-play.svg';
import Pause from '@/assets/pause.svg';

const theme = {
  components: {
    Slider: {
      colorFillContentHover: 'red',
      trackBg: 'rgba(22, 119, 255, 0.75)',
      railBg: 'rgba(0, 0, 0, 0.40)',
      railHoverBg: 'rgba(0, 0, 0, 0.75)',
      dotBorderColor: 'rgba(255, 0, 0, 0.5)',
    },
  },
};

interface PlayerProps {
  file: api.FileInfoGetResponse;
}

export const Player = ({ file }: PlayerProps) => {
  const [played, setPlayed] = useState(0);
  const [isPlaying, setPlaying] = useState(false);

  const player = useRef<ReactPlayer>();

  return (
    <Container>
      <div onClick={() => setPlaying(!isPlaying)}>
        <ReactPlayer
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          ref={player as any}
          onProgress={(state) => setPlayed(state.played)}
          url={file.link}
          playing={isPlaying}
          onEnded={() => setPlaying(false)}
          height={360}
          width={640}
          progressInterval={10}
        />
      </div>
      <ConfigProvider theme={theme}>
        <ActionsBox>
          <Flex gap="16px">
            {isPlaying ? (
              <PlayButton onClick={() => setPlaying(!isPlaying)} src={Pause} />
            ) : (
              <PlayButton onClick={() => setPlaying(!isPlaying)} src={Play} />
            )}

            <Slider
              style={{ width: '100%', marginBottom: 0 }}
              value={played}
              min={0}
              max={1}
              step={0.000001}
              tooltip={{ formatter: null }}
              marks={file.marks.reduce(
                (a, mark) => ({ ...a, [mark]: <Mark /> }),
                {}
              )}
              onChange={(value) => {
                setPlayed(value);
                player.current?.seekTo(value);
              }}
            />
          </Flex>
        </ActionsBox>
      </ConfigProvider>
    </Container>
  );
};

const Container = styled.div`
  display: flex;
  flex-direction: column;
  max-width: 720px;
  background: rgba(0, 0, 0);
  box-shadow: 0 0 16px rgba(0, 0, 0, 0.2);
  border-radius: 2%;
  height: 360px;
`;

const Mark = styled.div`
  width: 2px;
  height: 12px;
  background: red;
  margin-top: -4px;
`;

const ActionsBox = styled.div`
  margin: -40px 16px 0;
`;

const PlayButton = styled.img`
  z-index: 1;
  opacity: 70%;
  width: 32px;
  filter: drop-shadow(0 0 16px rgba(255, 255, 255, 0.7));
  cursor: pointer;

  transition: 0.2s ease-out;

  & path {
    fill: red;
  }

  &:hover {
    opacity: 85%;
    filter: drop-shadow(0 0 8px rgba(200, 200, 255, 0.9));
  }

  &:active {
    opacity: 100%;
    filter: drop-shadow(0 0 4px rgba(22, 119, 255, 1));
  }
`;
