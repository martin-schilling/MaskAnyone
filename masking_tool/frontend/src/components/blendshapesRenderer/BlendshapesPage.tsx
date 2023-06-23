import { Doggo } from "./Dog"
// import {Character} from "./Character"
import {Character} from "./Character2"
import { Canvas } from '@react-three/fiber'
import { Color } from "three"

const BlendshapesPage = () => {
    return(
        <>
            <Canvas
              // camera={{ fov:45, rotation: [0,0,0], position: [0, 0, 10] }}
              camera={{ fov: 90 }} shadows
              style={{ backgroundColor: '#FAD972', height: 600 }}
            >
                <ambientLight intensity={0.5} />
                <pointLight position={[10, 10, 10]} color={new Color(1, 1, 0)} intensity={0.5} castShadow />
                <pointLight position={[-10, 0, 10]} color={new Color(1, 0, 0)} intensity={0.5} castShadow />
                <pointLight position={[0, 0, 10]} intensity={0.5} castShadow />
                <Character></Character>
            </Canvas>
        </>
    )
}

export default BlendshapesPage