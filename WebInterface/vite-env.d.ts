interface ImportMetaEnv {
    readonly HOST?: string;
    readonly PORT?: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv;
}