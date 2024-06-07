import { ConfigProvider, Layout } from 'antd';
import * as S from './app.styles';
import { Routing } from '../pages';
import { ThemeProvider } from 'styled-components';
import { blue } from '@ant-design/colors';
import ruRus from 'antd/locale/ru_RU';

const theme = {};

const headerStyle = {
  backgroundColor: blue.primary,
  padding: '0 32px',
};

const App = () => {
  const { Header, Footer, Content } = Layout;

  return (
    <ConfigProvider locale={ruRus}>
      <ThemeProvider theme={theme}>
        <S.Wrapper>
          <Header style={headerStyle}></Header>
          <Content style={{ padding: '48px' }}>
            <Routing />
          </Content>
          <Footer>{''}</Footer>
        </S.Wrapper>
      </ThemeProvider>
    </ConfigProvider>
  );
};

export default App;
