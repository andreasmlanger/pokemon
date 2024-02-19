import 'package:flutter/material.dart';
import 'dart:ui';
import 'package:pokemon/services/spinkit.dart';

// https://www.shadertoy.com/view/ldyBWD
const shaderFileName = 'pikachu.frag';

class ShaderController {
  late final AnimationController controller;
  final int startTime = DateTime.now().millisecondsSinceEpoch;

  ShaderController(TickerProvider vsync) {
    controller = AnimationController(
      duration: const Duration(seconds: 1),
      vsync: vsync,
    )..repeat();
  }

  void dispose() {
    controller.dispose();
  }
}

Widget ShaderWidget(context, shaderController) {
  return Scaffold(
    body: Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          SizedBox(
            width: MediaQuery.of(context).size.width,
            height: MediaQuery.of(context).size.height,
            child: FutureBuilder<FragmentShader>(
                future: _load(),
                builder: (context, snapshot) {
                  if (snapshot.hasData) {
                    final shader = snapshot.data!;
                    shader.setFloat(1, MediaQuery.of(context).size.width);
                    shader.setFloat(2, MediaQuery.of(context).size.height);
                    return AnimatedBuilder(
                        animation: shaderController.controller,
                        builder: (context, _) {
                          double _elapsedTimeInSeconds = (DateTime.now().millisecondsSinceEpoch - shaderController.startTime) / 1000;
                          shader.setFloat(0, _elapsedTimeInSeconds);
                          return CustomPaint(
                            painter: ShaderPainter(shader),
                          );
                        });
                  } else {
                    return defaultLoadingWidget();
                  }
                }),
          )
        ],
      ),
    ),
  );
}

class ShaderPainter extends CustomPainter {
  final FragmentShader shader;
  ShaderPainter(this.shader);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.drawRect(
      Rect.fromLTWH(0, 0, size.width, size.height),
      Paint()..shader = shader,
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return oldDelegate != this;
  }
}

Future<FragmentShader> _load() async {
  FragmentProgram program = await FragmentProgram.fromAsset('assets/shaders/$shaderFileName');
  return program.fragmentShader();
}
