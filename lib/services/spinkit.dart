import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

Widget defaultLoadingWidget() {
  return Scaffold(
    backgroundColor: Colors.purple[800],
    body: const SpinKitThreeBounce(
      color: Colors.white,
      size: 50.0,
    ),
  );
}
