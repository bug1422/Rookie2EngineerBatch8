export interface MenuButton {
    name: string;
    path: string;
    type: MenuButtonType;
}

export enum MenuButtonType {
    PUBLIC = 'public',
    PRIVATE = 'private',
}
