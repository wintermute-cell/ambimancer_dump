import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls';
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader'
import {
  EffectComposer,
  EffectPass,
  GodRaysEffect,
  RenderPass
} from "postprocessing";

let renderer;
let composer;

const aspectRatio = 16/10;
let viewWidth = window.innerWidth/2;
let viewHeight = viewWidth/aspectRatio;

function createLight(color, x, y, z, composer) {
  const intensity = 1;
  const distance = 10;
  const angle = Math.PI/2.5;
  const penumbra = 0.2;
  const decay = 1;
  let spotLight = new THREE.SpotLight(color, intensity, distance, angle, penumbra, decay);
  spotLight.position.set(x, y, z);
  spotLight.castShadow = true;
  scene.add(spotLight);
  const spotLightHelper = new THREE.SpotLightHelper(spotLight);
  //scene.add(spotLightHelper);

  const lightRadius = 0.6;
  const fixtureLength = 0.7;

  const geometry = new THREE.CylinderGeometry(lightRadius, lightRadius, fixtureLength, 8);
  const material = new THREE.MeshPhongMaterial( {color: 0x222222} );
  const cylinder = new THREE.Mesh(geometry, material);
  cylinder.position.set(x, y, z);
  cylinder.lookAt(0,0,0);
  cylinder.translateOnAxis(new THREE.Vector3(0,0,1), (-fixtureLength/2)-0.02);
  cylinder.rotateX(Math.PI/2);
  scene.add(cylinder);
  let circleGeo = new THREE.CircleGeometry(0.6,8);
  let circleMat = new THREE.MeshBasicMaterial({color: color});
  let circle = new THREE.Mesh(circleGeo, circleMat);
  circle.position.set(x, y, z);
  circle.lookAt(0,0,0);
  scene.add(circle);
  let godrayOpts = {
    height: 360,
    kernelSize: 2,
    density: 1,
    decay: 0.9,
    weight: 0.5,
    exposure: 0.4,
    samples: 20,
    clampMax: 0.95
  };
  let gre = new GodRaysEffect(camera, circle, godrayOpts);
  composer.addPass(new EffectPass(camera, gre));
}

//const geometry = new THREE.BoxGeometry();
//const cube = new THREE.Mesh(geometry, material);
//scene.add(cube);
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 4;
camera.position.y = 3;


const loader = new STLLoader()
loader.load(
  '/room_scaled.stl',
  function (geometry) {
    const material = new THREE.MeshPhongMaterial({ color: 0x806060 });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.rotation.x = -Math.PI/2;
    mesh.scale.set(2, 2, 2);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    scene.add(mesh)
  },
  (xhr) => {
    console.log((xhr.loaded / xhr.total) * 100 + '% loaded')
  },
  (error) => {
    console.log(error)
  }
)

const light = new THREE.AmbientLight( 0x404040 ); // soft white light
scene.add(light);


const animate = () => {
  requestAnimationFrame(animate);
  //cube.rotation.x += 0.01;
  //cube.rotation.y += 0.01;
  composer.render(scene, camera);
};

const resize = () => {
  viewWidth = window.innerWidth/2;
  viewHeight = viewWidth/aspectRatio;
  composer.setSize(viewWidth, viewHeight)
  camera.aspect = aspectRatio;
  camera.updateProjectionMatrix();
};

export const createScene = (el) => {
  renderer = new THREE.WebGLRenderer({  
    powerPreference: "high-performance",
    antialias: true,
    stencil: false,
    depth: false,
    canvas: el,
  });
  renderer.shadowMap.enabled = true;
  const controls = new OrbitControls( camera, renderer.domElement );
  composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));

  createLight(0xff0000, 2,  4, 2, composer);
  createLight(0x00ff00, -2, 4, 2, composer);
  createLight(0x0000ff, 2,  4, -3, composer);
  createLight(0x3f9295, -2, 4, -3, composer);
  resize();
  animate();
}

window.addEventListener('resize', resize);
