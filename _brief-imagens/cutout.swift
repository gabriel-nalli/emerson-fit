import Foundation
import Vision
import CoreImage
import AppKit

let args = CommandLine.arguments
guard args.count == 3 else { fputs("uso: cutout <in> <out.png>\n", stderr); exit(2) }
let inURL = URL(fileURLWithPath: args[1])
let outURL = URL(fileURLWithPath: args[2])

guard let src = CGImageSourceCreateWithURL(inURL as CFURL, nil),
      let cg = CGImageSourceCreateImageAtIndex(src, 0, nil) else {
    fputs("erro: nao consegui ler \(args[1])\n", stderr); exit(1)
}

let handler = VNImageRequestHandler(cgImage: cg, options: [:])
let req = VNGenerateForegroundInstanceMaskRequest()
do { try handler.perform([req]) } catch {
    fputs("erro vision: \(error)\n", stderr); exit(1)
}
guard let obs = req.results?.first else {
    fputs("erro: nenhum objeto detectado\n", stderr); exit(1)
}
let pb = try obs.generateMaskedImage(ofInstances: obs.allInstances,
                                     from: handler,
                                     croppedToInstancesExtent: false)
let ci = CIImage(cvPixelBuffer: pb)
let ctx = CIContext()
guard let out = ctx.createCGImage(ci, from: ci.extent) else {
    fputs("erro: falha ao converter\n", stderr); exit(1)
}
guard let dest = CGImageDestinationCreateWithURL(outURL as CFURL, "public.png" as CFString, 1, nil) else {
    fputs("erro: destino\n", stderr); exit(1)
}
CGImageDestinationAddImage(dest, out, nil)
CGImageDestinationFinalize(dest)
print("ok \(obs.allInstances.count) instancia(s) -> \(outURL.lastPathComponent)")
