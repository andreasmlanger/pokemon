import 'package:flutter/material.dart';
import 'package:pokemon/services/pokemon.dart';


class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {

  Map data = {};
  bool caught = false;
  List<Pokemon> pokemons = [];

  void load_pokemons() {
    setState(() {
      pokemons = data['pokemons'].where((p) => p.caught == caught).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    final routeArguments = ModalRoute.of(context)?.settings.arguments;
    data = data.isNotEmpty ? data : routeArguments as Map<String, dynamic>? ?? {};
    load_pokemons();

    void update_pokemon_list() {
      setState(() {
        caught = !caught;
        load_pokemons();
      });
    }

    return Scaffold(
      appBar: AppBar(
        title: Text(
          caught ? 'Pokémon (caught)' : 'Pokémon',
          style: TextStyle(
            color: Colors.white,
            fontFamily: 'Nunito',
            fontSize: 24.0,
            fontWeight: FontWeight.w400,
          )
        ),
        backgroundColor: Colors.purple[800],
        actions: <Widget>[
          TextButton.icon(
            label: const Text(''),
            icon: const Icon(Icons.refresh),
            style: ButtonStyle(
              foregroundColor: MaterialStateProperty.all(Colors.white),
            ),
            onPressed: () {
              // Navigate to Loading Screen
              Navigator.of(context).pushReplacementNamed('/');
            },
          ),
          TextButton.icon(
            label: const Text(''),
            icon: Icon(caught ? Icons.catching_pokemon : Icons.panorama_fish_eye),
            style: ButtonStyle(
              foregroundColor: MaterialStateProperty.all(Colors.white),
            ),
            onPressed: () {
              update_pokemon_list();
            }
          )
        ],
      ),
      body: ListView.builder(
        itemCount: pokemons.length,
        itemBuilder: (context, index) {
          Pokemon pokemon = pokemons[index];
          Color? bgColor = Colors.white;
          return Dismissible(
            key: Key(pokemon.id.toString()),
            direction: DismissDirection.endToStart,
            onDismissed: (direction) {
              if (direction == DismissDirection.endToStart) {
                pokemon.toggle_caught(pokemon.caught);
                setState(() {
                  pokemons.removeAt(index);
                });
              }
            },
            background: Container(
              color: caught ? Colors.red : Colors.green,
              child: Icon(
                caught ? Icons.close : Icons.done,
                color: Colors.white,
              ),
              alignment: Alignment.centerRight,
              padding: EdgeInsets.only(right: 10.0),
            ),
            child: Card (
              elevation: 5,
              child: ListTile(
                tileColor: bgColor,
                title: Text(
                  pokemon.name,
                  style: TextStyle(
                    fontFamily: 'Nunito',
                    fontSize: 20.0,
                    fontWeight: FontWeight.w400,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                subtitle: Text(
                  pokemon.form,
                  style: TextStyle(
                    fontFamily: 'Nunito',
                    fontSize: 14.0,
                    fontWeight: FontWeight.w400,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                leading: Stack(
                  children: [
                    // Background image
                    Image.asset(
                      pokemon.get_bg_image_path(),
                      fit: BoxFit.fitHeight,
                    ),
                    // Foreground image
                    Image.asset(
                      pokemon.get_image_path(),
                      fit: BoxFit.fitHeight,
                    ),
                  ],
                ),
                trailing: Text(
                  pokemon.idx.toString(),
                  style: TextStyle(
                    fontFamily: 'Nunito',
                    fontSize: 18.0,
                    fontWeight: FontWeight.w400,
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
