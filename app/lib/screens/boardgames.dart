import 'package:amplify_api/amplify_api.dart';
import 'package:app/models/BoardGame.dart';
import 'package:app/models/BoardGameType.dart';
import 'package:flutter/material.dart';
import 'package:amplify_api/amplify_api.dart';
import 'package:amplify_flutter/amplify_flutter.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class BoardGamesScreen extends StatefulWidget {
  const BoardGamesScreen({
    super.key,
  });

  @override
  State<BoardGamesScreen> createState() => _BoardGamesScreenState();
}

class _BoardGamesScreenState extends State<BoardGamesScreen> {
  var _boardgames = <BoardGame>[];

  bool _showSubmitForm = false;

  @override
  void initState() {
    super.initState();
    _fetchBoardGames();
  }

  Future<void> _fetchBoardGames() async {
    safePrint('Getting boardgames');
    bool signedInUser = false;
    try {
      final result = await Amplify.Auth.fetchAuthSession();
      safePrint('User is signed in: ${result.isSignedIn}');
      signedInUser = result.isSignedIn;
    } on AuthException catch (e) {
      safePrint('Error retrieving auth session: ${e.message}');
    }

    try {
      final request = ModelQueries.list(BoardGame.classType,
          authorizationMode: signedInUser
              ? APIAuthorizationType.userPools
              : APIAuthorizationType.iam);

      final response = await Amplify.API.query(request: request).response;
      final games = response.data?.items;

      if (response.hasErrors) {
        safePrint('errors: ${response.errors}');
        return;
      }
      if (games!.isEmpty) {
        safePrint('no boardgames yet');
      }
      setState(() {
        _boardgames = games!.whereType<BoardGame>().toList();
      });
    } on ApiException catch (e) {
      safePrint('Query failed: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text('BoardGames'),
        ),
        floatingActionButton: FloatingActionButton(
          onPressed: () {
            setState(() {
              _showSubmitForm = !_showSubmitForm;
            });
          },
          child: Icon(_showSubmitForm ? Icons.close : Icons.add),
        ),
        body: Column(children: [
          Expanded(
            child: GridView.builder(
              itemCount: _boardgames.length,
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                mainAxisSpacing: 8.0,
                crossAxisSpacing: 8.0,
                childAspectRatio: 1.0,
              ),
              itemBuilder: (BuildContext context, int index) {
                return Container(
                  color: Colors.blue,
                  child: Center(
                    child: Text(
                      _boardgames[index].name,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 18.0,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          if (_showSubmitForm) _SubmitForm(_fetchBoardGames),
        ]));
  }
}

class _SubmitForm extends StatefulWidget {
  final Future<void> Function() toCallAfterSubmission;

  const _SubmitForm(this.toCallAfterSubmission);

  @override
  _SubmitFormState createState() => _SubmitFormState();
}

class _SubmitFormState extends State<_SubmitForm> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _descriptionController = TextEditingController();
  final TextEditingController _minimumNumberOfPlayersController =
      TextEditingController();
  final TextEditingController _minimumDurationController =
      TextEditingController();
  final TextEditingController _maximumNumberOfPlayersController =
      TextEditingController();
  final TextEditingController _maximumDurationController =
      TextEditingController();

// controllers don't work with dropdown fields
  BoardGameType? _boardgameType;

  @override
  void dispose() {
    _nameController.dispose();
    _descriptionController.dispose();
    _minimumNumberOfPlayersController.dispose();
    _minimumDurationController.dispose();
    _maximumNumberOfPlayersController.dispose();
    _maximumDurationController.dispose();
    super.dispose();
  }

  Future<void> submitForm() async {
    var currentState = _formKey.currentState;
    // type narrowing, remove nullable
    if (currentState == null) {
      return;
    }

    if (!currentState.validate()) {
      return;
    }
    //need to explicitly save state for _boargameType
    currentState.save();

    final name = _nameController.text;
    final description = _descriptionController.text;
    final minimumNumberOfPlayers =
        int.parse(_minimumNumberOfPlayersController.text);
    final minimumDuration = int.parse(_minimumDurationController.text);
    final BoardGameType type =
        _boardgameType!; //it cannot be null due to form validation
    final maximumNumberOfPlayers =
        int.parse(_maximumNumberOfPlayersController.text);
    final maximumDuration = int.parse(_maximumDurationController.text);

    // Perform form submission with the entered values
    // You can send the data to your GraphQL endpoint here
    final newBoardgame = BoardGame(
        name: name,
        description: description,
        minimumNumberOfPlayers: minimumNumberOfPlayers,
        maximumNumberOfPlayers: maximumNumberOfPlayers,
        minimumDuration: minimumDuration,
        maximumDuration: maximumDuration,
        type: type);
    final request = ModelMutations.create(newBoardgame);
    final response = await Amplify.API.mutate(request: request).response;
    safePrint('Create result: $response');

    widget.toCallAfterSubmission();

    // Reset the form after submission
    _formKey.currentState?.reset();

    // Clear the form field values
    _nameController.clear();
    _descriptionController.clear();
    _minimumNumberOfPlayersController.clear();
    _minimumDurationController.clear();
    _maximumNumberOfPlayersController.clear();
    _maximumDurationController.clear();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16.0),
      child: Form(
        key: _formKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Add boardgame',
              style: TextStyle(
                fontSize: 20.0,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16.0),
            TextFormField(
              controller: _nameController,
              decoration: const InputDecoration(labelText: 'Name'),
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter a name';
                }
                return null;
              },
            ),
            TextFormField(
              controller: _descriptionController,
              decoration: const InputDecoration(labelText: 'Description'),
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter a description';
                }
                return null;
              },
            ),
            TextFormField(
              controller: _minimumNumberOfPlayersController,
              decoration:
                  const InputDecoration(labelText: 'Minimum Number of Players'),
              keyboardType: TextInputType.number,
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter the minimum number of players';
                }
                return null;
              },
            ),
            TextFormField(
              controller: _maximumNumberOfPlayersController,
              decoration: const InputDecoration(
                  labelText: 'Maximum Number of Players (Optional)'),
              keyboardType: TextInputType.number,
            ),
            TextFormField(
              controller: _minimumDurationController,
              decoration: const InputDecoration(
                  labelText: 'Minimum Duration in minutes'),
              keyboardType: TextInputType.number,
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Please enter the minimum duration';
                }
                return null;
              },
            ),
            TextFormField(
              controller: _maximumDurationController,
              decoration: const InputDecoration(
                  labelText: 'Maximum Duration in minutes (Optional)'),
              keyboardType: TextInputType.number,
            ),
            DropdownButtonFormField<BoardGameType>(
              value: _boardgameType,
              onChanged: (BoardGameType? newValue) {
                setState(() {
                  _boardgameType = newValue;
                });
              },
              validator: (value) {
                if (value == null) {
                  return 'Please select a type';
                }
                return null;
              },
              decoration: const InputDecoration(labelText: 'Type of boardgame'),
              items: BoardGameType.values.map((type) {
                return DropdownMenuItem<BoardGameType>(
                  value: type,
                  child: Text(type.toString().split('.').last),
                );
              }).toList(),
            ),
            const SizedBox(height: 16.0),
            ElevatedButton(
              onPressed: submitForm,
              child: const Text('Submit'),
            ),
          ],
        ),
      ),
    );
  }
}
// class GridListDemo extends StatelessWidget {
//   const GridListDemo({super.key});

//   List<_Photo> _photos(BuildContext context) {
//     final localizations = GalleryLocalizations.of(context)!;
//     return [
//       _Photo(
//         assetName: 'places/india_chennai_flower_market.png',
//         title: localizations.placeChennai,
//         subtitle: localizations.placeFlowerMarket,
//       ),
//       _Photo(
//         assetName: 'places/india_tanjore_bronze_works.png',
//         title: localizations.placeTanjore,
//         subtitle: localizations.placeBronzeWorks,
//       ),
//       _Photo(
//         assetName: 'places/india_tanjore_market_merchant.png',
//         title: localizations.placeTanjore,
//         subtitle: localizations.placeMarket,
//       ),
//       _Photo(
//         assetName: 'places/india_tanjore_thanjavur_temple.png',
//         title: localizations.placeTanjore,
//         subtitle: localizations.placeThanjavurTemple,
//       ),
//       _Photo(
//         assetName: 'places/india_tanjore_thanjavur_temple_carvings.png',
//         title: localizations.placeTanjore,
//         subtitle: localizations.placeThanjavurTemple,
//       ),
//       _Photo(
//         assetName: 'places/india_pondicherry_salt_farm.png',
//         title: localizations.placePondicherry,
//         subtitle: localizations.placeSaltFarm,
//       ),
//       _Photo(
//         assetName: 'places/india_chennai_highway.png',
//         title: localizations.placeChennai,
//         subtitle: localizations.placeScooters,
//       ),
//       _Photo(
//         assetName: 'places/india_chettinad_silk_maker.png',
//         title: localizations.placeChettinad,
//         subtitle: localizations.placeSilkMaker,
//       ),
//       _Photo(
//         assetName: 'places/india_chettinad_produce.png',
//         title: localizations.placeChettinad,
//         subtitle: localizations.placeLunchPrep,
//       ),
//       _Photo(
//         assetName: 'places/india_tanjore_market_technology.png',
//         title: localizations.placeTanjore,
//         subtitle: localizations.placeMarket,
//       ),
//       _Photo(
//         assetName: 'places/india_pondicherry_beach.png',
//         title: localizations.placePondicherry,
//         subtitle: localizations.placeBeach,
//       ),
//       _Photo(
//         assetName: 'places/india_pondicherry_fisherman.png',
//         title: localizations.placePondicherry,
//         subtitle: localizations.placeFisherman,
//       ),
//     ];
//   }

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(
//         automaticallyImplyLeading: false,
//         title: Text(GalleryLocalizations.of(context)!.demoGridListsTitle),
//       ),
//       body: GridView.count(
//         restorationId: 'grid_view_demo_grid_offset',
//         crossAxisCount: 2,
//         mainAxisSpacing: 8,
//         crossAxisSpacing: 8,
//         padding: const EdgeInsets.all(8),
//         childAspectRatio: 1,
//         children: _photos(context).map<Widget>((photo) {
//           return _GridDemoPhotoItem(
//             photo: photo,
//             tileStyle: type,
//           );
//         }).toList(),
//       ),
//     );
//   }
// }

// class _Photo {
//   _Photo({
//     required this.assetName,
//     required this.title,
//     required this.subtitle,
//   });

//   final String assetName;
//   final String title;
//   final String subtitle;
// }

// /// Allow the text size to shrink to fit in the space
// class _GridTitleText extends StatelessWidget {
//   const _GridTitleText(this.text);

//   final String text;

//   @override
//   Widget build(BuildContext context) {
//     return FittedBox(
//       fit: BoxFit.scaleDown,
//       alignment: AlignmentDirectional.centerStart,
//       child: Text(text),
//     );
//   }
// }

// class _GridDemoPhotoItem extends StatelessWidget {
//   const _GridDemoPhotoItem({
//     required this.photo,
//   });

//   final _Photo photo;

//   @override
//   Widget build(BuildContext context) {
//     final Widget image = Semantics(
//       label: '${photo.title} ${photo.subtitle}',
//       child: Material(
//         shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
//         clipBehavior: Clip.antiAlias,
//         child: Image.asset(
//           photo.assetName,
//           package: 'flutter_gallery_assets',
//           fit: BoxFit.cover,
//         ),
//       ),
//     );

//     return GridTile(
//       footer: Material(
//         color: Colors.transparent,
//         shape: const RoundedRectangleBorder(
//           borderRadius: BorderRadius.vertical(bottom: Radius.circular(4)),
//         ),
//         clipBehavior: Clip.antiAlias,
//         child: GridTileBar(
//           backgroundColor: Colors.black45,
//           title: _GridTitleText(photo.title),
//           subtitle: _GridTitleText(photo.subtitle),
//         ),
//       ),
//       child: image,
//     );
//   }
// }
