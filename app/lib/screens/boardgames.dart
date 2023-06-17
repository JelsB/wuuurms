import 'package:amplify_api/amplify_api.dart';
import 'package:app/models/BoardGame.dart';
import 'package:app/models/BoardGameType.dart';
import 'package:app/widgets/appBar.dart';
import 'package:flutter/material.dart';
import 'package:amplify_flutter/amplify_flutter.dart';

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

  bool _userIsSignedIn = false;

  /// Indicates if user login state has been checked explicitly
  ///
  /// This is useful to avoid relying on asyn operations to check this
  bool _initialCheckIfUserIsSignedInIsDone = false;

  @override
  void initState() {
    super.initState();
    _checkIfUserIsSignedIn();
    _fetchBoardGames();
  }

  Future<void> _checkIfUserIsSignedIn() async {
    var signedIn = false;
    try {
      final result = await Amplify.Auth.fetchAuthSession();
      safePrint('User is signed in: ${result.isSignedIn}');
      signedIn = result.isSignedIn;
    } on AuthException catch (e) {
      safePrint('Error retrieving auth session: ${e.message}');
    }

    setState(() {
      _userIsSignedIn = signedIn;
      _initialCheckIfUserIsSignedInIsDone = true;
    });
  }

  Future<void> _fetchBoardGames() async {
    safePrint('Getting boardgames');

    // if a user's login state has not been determined at least once,
    // explitly check it and wait for response
    // to avoid race conditions where the user is actually logged in
    // but the `_userIsSignedIn` is not updated yet.
    // In the future, this could be avoided with global state
    // management in this app.
    if (!_initialCheckIfUserIsSignedInIsDone) {
      await _checkIfUserIsSignedIn();
    }

    final request = ModelQueries.list(BoardGame.classType,
        authorizationMode: _userIsSignedIn
            ? APIAuthorizationType.userPools
            : APIAuthorizationType.iam);
    try {
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

  List<_BoardGameItem> _boardGameItems() {
    var counter = 0;
    List<_BoardGameItem> modifiedList = _boardgames.map((game) {
      var assetName =
          'lib/assets/local_tests/boardgame_image/${counter % 5}.jpg';
      counter++;
      return _BoardGameItem(boardgame: game, assetName: assetName);
    }).toList();
    return modifiedList;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: const MyAppBar(title: 'Boardgames'),
        floatingActionButton: _userIsSignedIn
            ? FloatingActionButton(
                onPressed: () {
                  setState(() {
                    _showSubmitForm = !_showSubmitForm;
                  });
                },
                child: Icon(_showSubmitForm ? Icons.close : Icons.add),
              )
            : null,
        body: Stack(children: [
          GridView.count(
            restorationId: 'grid_view_demo_grid_offset',
            crossAxisCount: 2,
            mainAxisSpacing: 8,
            crossAxisSpacing: 8,
            padding: const EdgeInsets.all(8),
            childAspectRatio: 1,
            children: _boardGameItems().map<Widget>((game) {
              return _GridDemoPhotoItem(
                boardgameItem: game,
                // tileStyle: type,
              );
            }).toList(),
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
      color: Colors.white,
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

class _BoardGameItem {
  _BoardGameItem({required this.boardgame, required this.assetName});

  final BoardGame boardgame;
  final String assetName;
}

/// Allow the text size to shrink to fit in the space
class _GridTitleText extends StatelessWidget {
  const _GridTitleText(this.text);

  final String text;

  @override
  Widget build(BuildContext context) {
    return FittedBox(
      fit: BoxFit.scaleDown,
      alignment: AlignmentDirectional.centerStart,
      child: Text(text),
    );
  }
}

class _GridDemoPhotoItem extends StatelessWidget {
  const _GridDemoPhotoItem({
    required this.boardgameItem,
  });

  final _BoardGameItem boardgameItem;

  @override
  Widget build(BuildContext context) {
    final Widget image = Semantics(
      label: boardgameItem.boardgame.name,
      child: Material(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
        clipBehavior: Clip.antiAlias,
        child: Image.asset(
          boardgameItem.assetName,
          // package: 'flutter_gallery_assets',
          fit: BoxFit.cover,
        ),
      ),
    );

    return GridTile(
      footer: Material(
        color: Colors.transparent,
        shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.vertical(bottom: Radius.circular(4)),
        ),
        clipBehavior: Clip.antiAlias,
        child: GridTileBar(
          backgroundColor: Colors.black45,
          title: _GridTitleText(boardgameItem.boardgame.name),
          // subtitle: _GridTitleText(photo.subtitle),
        ),
      ),
      child: image,
    );
  }
}
