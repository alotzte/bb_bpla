import { Button, ConfigProvider, Flex, Layout } from 'antd';
import * as S from './app.styles';
import { Routing } from '../pages';
import { ThemeProvider } from 'styled-components';
import { blue } from '@ant-design/colors';
import ruRus from 'antd/locale/ru_RU';
import telegram from '@/assets/telegram.svg';

const theme = {};

const headerStyle = {
  backgroundColor: blue.primary,
  padding: '0 32px',
};

const icon = {
  width: '24px',
  marginLeft: '-4px',
};

const flex = {
  height: '100%',
};

const App = () => {
  const { Header, Content } = Layout;

  return (
    <ConfigProvider locale={ruRus}>
      <ThemeProvider theme={theme}>
        <S.Wrapper>
          <Header style={headerStyle}>
            <Flex justify="end" align="center" style={flex}>
              <Button
                type="primary"
                shape="circle"
                icon={<img src={telegram} style={icon} />}
                href="https://t.me/lct24_bb_bot"
                target="_blank"
              />
            </Flex>
          </Header>
          <Content style={{ padding: '48px' }}>
            <Routing />
          </Content>
        </S.Wrapper>
      </ThemeProvider>
    </ConfigProvider>
  );
};

export default App;
