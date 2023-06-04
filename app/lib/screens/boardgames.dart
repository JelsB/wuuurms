import 'package:amplify_api/amplify_api.dart';
import 'package:app/models/BoardGame.dart';
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

  @override
  void initState() {
    super.initState();
    _fetchBoardGames();
  }

  Future<void> _fetchBoardGames() async {
    safePrint('Getting boardgames');
    try {
      final result = await Amplify.Auth.fetchAuthSession();
      safePrint('User is signed in: ${result.isSignedIn}');
    } on AuthException catch (e) {
      safePrint('Error retrieving auth session: ${e.message}');
    }

    try {
      final request = ModelQueries.list(BoardGame.classType,
          authorizationMode: APIAuthorizationType.iam);
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
      body: GridView.builder(
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
