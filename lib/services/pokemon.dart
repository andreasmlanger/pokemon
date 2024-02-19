import 'package:postgres/postgres.dart';
import 'package:pokemon/services/storage.dart';

String zfill(int length, String text) {
  if (text.length >= length) {
    return text;
  } else {
    String zeros = '0' * (length - text.length);
    return zeros + text;
  }
}

class Pokemon {
  final int id;
  final int idx;
  final String name;
  final String type;
  final String form;
  bool caught;

  Pokemon({
    required this.id,
    required this.idx,
    required this.name,
    required this.type,
    required this.form,
    required this.caught,
  });

  String get_image_path() {
    String file_name = this.idx.toString();
    file_name = zfill(4, file_name);
    if (this.form != '') {
      file_name = file_name + '_' + this.form;
    }
    return 'assets/images/' + file_name + '.png';
  }

  String get_bg_image_path() {
    return 'assets/images/' + this.type + '.png';
  }

  void toggle_caught(caught) async {
    this.caught = !caught;
    String q = 'UPDATE "public"."pokemon" SET caught = @caught WHERE id = @id';
    executeSqlQuery(q);
  }

  void executeSqlQuery(String q) async {
    Connection conn = await connectToDatabase();
    await conn.execute(Sql.named(q), parameters: {'id': id, 'caught': caught});
    await conn.close();
  }
}

class Pokemons {
  late List<Pokemon> pokemons;

  Future<void> getCaughtPokemon() async {
    Connection conn = await connectToDatabase();
    String q = 'SELECT * FROM "public"."pokemon" ORDER BY id';
    final results = await conn.execute(q);

    pokemons = results.map((row) {
      return Pokemon(
        id: row[0] as int,
        idx: row[1] as int,
        name: row[2] as String,
        type: row[3] as String,
        form: row[4] != null ? row[4] as String : '',
        caught: row[5] as bool,
      );
    }).toList();

    await conn.close();
  }
}
