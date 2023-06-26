import 'package:app/models/user_login_state.dart';
import 'package:app/widgets/app_bar.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({
    super.key,
  });

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  @override
  void initState() {
    super.initState();
    //When getting to this page, it means that the use has logged in because
    // it's and authenticated view. Ideally, this would be set on the
    // authenticatedView Widget, but I don't know how
    // This also gives exceptions... :/
    // Provider.of<UserLoginStateModel>(context, listen: true).changeTo(true);
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      appBar: MyAppBar(title: 'Profile'),
    );
  }
}
