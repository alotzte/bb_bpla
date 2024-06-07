import { FileTablePage } from '@/pages/file-table';

interface RouteItem {
  path: string;
  element: JSX.Element;
  name: string;
}

export const routes: RouteItem[] = [
  {
    path: '/',
    element: <FileTablePage />,
    name: 'FileTable',
  },
];
