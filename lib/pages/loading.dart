import 'package:flutter/material.dart';
import 'package:pokemon/services/pokemon.dart';
import 'package:pokemon/services/shader.dart';


class Loading extends StatefulWidget {
  const Loading({Key? key}) : super(key: key);
  @override
  State<Loading> createState() => _LoadingState();
}

class _LoadingState extends State<Loading> with TickerProviderStateMixin {
  late List<Pokemon> pokemons;
  late ShaderController shaderController;

  @override
  void initState() {
    super.initState();
    shaderController = ShaderController(this);
    setupPokemon();
  }

  @override
  void dispose() {
    shaderController.dispose();
    super.dispose();
  }

  void setupPokemon() async {
    Pokemons instance = Pokemons();
    await instance.getCaughtPokemon();
    pokemons = instance.pokemons;
    navigateToHome();
  }

  void navigateToHome() {
    Future.delayed(Duration.zero, () {
      Navigator.pushReplacementNamed(context, '/home', arguments: {
        'pokemons': pokemons,
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return ShaderWidget(context, shaderController);
  }
}

