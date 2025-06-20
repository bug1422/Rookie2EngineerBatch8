import { MenuButton, MenuButtonType } from '@/types/menuButton';

export const menuButtons: MenuButton[] = [
    {
        name: 'Home',
        path: '/',
        type: MenuButtonType.PUBLIC,
    },
    {
        name: 'Manage User',
        path: '/manage-user',
        type: MenuButtonType.PRIVATE,
    },
    {
        name: 'Manage Asset',
        path: '/manage-asset',
        type: MenuButtonType.PRIVATE,
    },
    {
        name: 'Manage Assignment',
        path: '/manage-assignment',
        type: MenuButtonType.PRIVATE,
    },
    {
        name: 'Request for Returning',
        path: '/request-for-returning',
        type: MenuButtonType.PUBLIC,
    },
    {
        name: 'Report',
        path: '/report',
        type: MenuButtonType.PRIVATE,
    },
];
