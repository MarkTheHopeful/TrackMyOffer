import { FetchHelloButton } from "../components/FetchHelloButton.tsx";
import {FetchFeaturesHelloButton} from "../components/FetchFeaturesHelloButton.tsx";

export default function Home() {
    return (
        <main style={{ padding: "2rem" }}>
            <h1>Frontend Boilerplate</h1>
            <FetchHelloButton />
            <FetchFeaturesHelloButton />
        </main>
    );
}
