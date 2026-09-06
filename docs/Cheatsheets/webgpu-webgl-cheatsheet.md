---
layout: default
title: "WebGPU & WebGL Graphics Programming Cheatsheet"
---

# WebGPU & WebGL Graphics Programming Cheatsheet

WebGPU is the modern W3C standard offering low-overhead, high-performance direct access to GPU hardware for both rendering and compute shaders in web browsers. WebGL is the legacy HTML5 graphics standard based on OpenGL ES.

---

## 1. WebGPU Architecture & Pipeline Flow

```mermaid
graph TD
    JS[JavaScript Engine] --> Adapter[navigator.gpu.requestAdapter()]
    Adapter --> Device[adapter.requestDevice()]

    Device --> ShaderModule[device.createShaderModule WGSL Shaders]
    Device --> Buffers[device.createBuffer GPU Memory]
    Device --> Textures[device.createTexture GPU Textures]

    ShaderModule --> Pipeline[device.createRenderPipeline / createComputePipeline]
    Buffers --> BindGroup[device.createBindGroup Resource Bindings]
    Textures --> BindGroup

    Pipeline --> CommandEncoder[device.createCommandEncoder()]
    BindGroup --> CommandEncoder

    CommandEncoder --> PassEncoder[beginRenderPass / beginComputePass]
    PassEncoder --> Submit[device.queue.submit commandBuffers]
    Submit --> GPUHardware[GPU Hardware Execution]
```

---

## 2. WebGPU WGSL Compute Shader (`shader.wgsl`)

```wgsl
// WebGPU Shading Language (WGSL) Compute Shader
@group(0) @binding(0) var<storage, read> inputData : array<f32>;
@group(0) @binding(1) var<storage, read_write> outputData : array<f32>;

@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) global_id : vec3<u32>) {
    let index : u32 = global_id.x;
    if (index >= arrayLength(&inputData)) {
        return;
    }
    // High-performance parallel computation on GPU
    outputData[index] = inputData[index] * 2.5 + 1.0;
}
```

---

## 3. WebGPU JavaScript Initialization & Execution

```typescript
async function runWebGPUCompute() {
  if (!navigator.gpu) {
    throw new Error("WebGPU is not supported on this browser.");
  }

  const adapter = await navigator.gpu.requestAdapter();
  const device = await adapter.requestDevice();

  // 1. Prepare Data & GPU Buffers
  const inputValues = new Float32Array([1.0, 2.0, 3.0, 4.0, 5.0]);
  const gpuBufferInput = device.createBuffer({
    size: inputValues.byteLength,
    usage: GPUBufferUsage.STORAGE | GPUBufferUsage.COPY_DST,
  });
  device.queue.writeBuffer(gpuBufferInput, 0, inputValues);

  const gpuBufferOutput = device.createBuffer({
    size: inputValues.byteLength,
    usage: GPUBufferUsage.STORAGE | GPUBufferUsage.COPY_SRC,
  });

  // 2. Load WGSL Shader Module
  const shaderModule = device.createShaderModule({
    code: `
      @group(0) @binding(0) var<storage, read> inputData : array<f32>;
      @group(0) @binding(1) var<storage, read_write> outputData : array<f32>;

      @compute @workgroup_size(64)
      fn main(@builtin(global_invocation_id) global_id : vec3<u32>) {
          let i = global_id.x;
          outputData[i] = inputData[i] * 2.0;
      }
    `
  });

  // 3. Create Compute Pipeline & Bind Group
  const computePipeline = device.createComputePipeline({
    layout: 'auto',
    compute: { module: shaderModule, entryPoint: 'main' },
  });

  const bindGroup = device.createBindGroup({
    layout: computePipeline.getBindGroupLayout(0),
    entries: [
      { binding: 0, resource: { buffer: gpuBufferInput } },
      { binding: 1, resource: { buffer: gpuBufferOutput } },
    ],
  });

  // 4. Encode & Submit Commands to GPU Queue
  const commandEncoder = device.createCommandEncoder();
  const passEncoder = commandEncoder.beginComputePass();
  passEncoder.setPipeline(computePipeline);
  passEncoder.setBindGroup(0, bindGroup);
  passEncoder.dispatchWorkgroups(Math.ceil(inputValues.length / 64));
  passEncoder.end();

  device.queue.submit([commandEncoder.finish()]);
  console.log("WebGPU compute pipeline executed successfully!");
}
```

---

## 4. WebGL vs WebGPU Feature Comparison

| Feature / Metric | WebGL 2.0 | WebGPU |
| :--- | :--- | :--- |
| **Underlying Native API** | OpenGL ES 3.0 | Vulkan / Metal / DirectX 12 |
| **Compute Shaders** | Very limited / Workarounds | Native, First-Class Compute Shaders |
| **Shading Language** | GLSL ES 3.00 | WGSL (WebGPU Shading Language) |
| **CPU Overhead** | High (Global State Machine) | Minimal (Stateless Pipeline Objects) |
| **Multithreading** | Single-threaded DOM main thread | Multi-threaded Command Encoding via Web Workers |
| **Memory Management** | Browser Garbage Collected | Explicit GPU Buffer Allocation & Bind Groups |

---

## Related Cheatsheets

- [Master Index](../Cheatsheets.md)
- [PWA & WebAssembly Cheatsheet](pwa-webassembly-cheatsheet.md)
- [JavaScript Cheatsheet](javascript-cheatsheet.md)
- [Web Performance Optimization Cheatsheet](web-performance-optimization-cheatsheet.md)
