/*
* Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
*
* Licensed under the Apache License, Version 2.0 (the "License").
* You may not use this file except in compliance with the License.
* A copy of the License is located at
*
*  http://aws.amazon.com/apache2.0
*
* or in the "license" file accompanying this file. This file is distributed
* on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
* express or implied. See the License for the specific language governing
* permissions and limitations under the License.
*/

// NOTE: This file is generated and may not follow lint rules defined in your app
// Generated files can be excluded from analysis in analysis_options.yaml
// For more info, see: https://dart.dev/guides/language/analysis-options#excluding-code-from-analysis

// ignore_for_file: public_member_api_docs, annotate_overrides, dead_code, dead_codepublic_member_api_docs, depend_on_referenced_packages, file_names, library_private_types_in_public_api, no_leading_underscores_for_library_prefixes, no_leading_underscores_for_local_identifiers, non_constant_identifier_names, null_check_on_nullable_type_parameter, prefer_adjacent_string_concatenation, prefer_const_constructors, prefer_if_null_operators, prefer_interpolation_to_compose_strings, slash_for_doc_comments, sort_child_properties_last, unnecessary_const, unnecessary_constructor_name, unnecessary_late, unnecessary_new, unnecessary_null_aware_assignments, unnecessary_nullable_for_final_variable_declarations, unnecessary_string_interpolations, use_build_context_synchronously

import 'package:amplify_core/amplify_core.dart';
import 'package:flutter/foundation.dart';


/** This is an auto generated class representing the BoardGame type in your schema. */
@immutable
class BoardGame extends Model {
  static const classType = const _BoardGameModelType();
  final String id;
  final String? _name;
  final String? _description;
  final int? _minimumNumberOfPlayers;
  final int? _maximumNumberOfPlayers;
  final int? _minimumDuration;
  final int? _maximumDuration;
  final TemporalDateTime? _createdAt;
  final TemporalDateTime? _updatedAt;

  @override
  getInstanceType() => classType;
  
  @Deprecated('[getId] is being deprecated in favor of custom primary key feature. Use getter [modelIdentifier] to get model identifier.')
  @override
  String getId() => id;
  
  BoardGameModelIdentifier get modelIdentifier {
      return BoardGameModelIdentifier(
        id: id
      );
  }
  
  String get name {
    try {
      return _name!;
    } catch(e) {
      throw new AmplifyCodeGenModelException(
          AmplifyExceptionMessages.codeGenRequiredFieldForceCastExceptionMessage,
          recoverySuggestion:
            AmplifyExceptionMessages.codeGenRequiredFieldForceCastRecoverySuggestion,
          underlyingException: e.toString()
          );
    }
  }
  
  String get description {
    try {
      return _description!;
    } catch(e) {
      throw new AmplifyCodeGenModelException(
          AmplifyExceptionMessages.codeGenRequiredFieldForceCastExceptionMessage,
          recoverySuggestion:
            AmplifyExceptionMessages.codeGenRequiredFieldForceCastRecoverySuggestion,
          underlyingException: e.toString()
          );
    }
  }
  
  int get minimumNumberOfPlayers {
    try {
      return _minimumNumberOfPlayers!;
    } catch(e) {
      throw new AmplifyCodeGenModelException(
          AmplifyExceptionMessages.codeGenRequiredFieldForceCastExceptionMessage,
          recoverySuggestion:
            AmplifyExceptionMessages.codeGenRequiredFieldForceCastRecoverySuggestion,
          underlyingException: e.toString()
          );
    }
  }
  
  int? get maximumNumberOfPlayers {
    return _maximumNumberOfPlayers;
  }
  
  int get minimumDuration {
    try {
      return _minimumDuration!;
    } catch(e) {
      throw new AmplifyCodeGenModelException(
          AmplifyExceptionMessages.codeGenRequiredFieldForceCastExceptionMessage,
          recoverySuggestion:
            AmplifyExceptionMessages.codeGenRequiredFieldForceCastRecoverySuggestion,
          underlyingException: e.toString()
          );
    }
  }
  
  int? get maximumDuration {
    return _maximumDuration;
  }
  
  TemporalDateTime? get createdAt {
    return _createdAt;
  }
  
  TemporalDateTime? get updatedAt {
    return _updatedAt;
  }
  
  const BoardGame._internal({required this.id, required name, required description, required minimumNumberOfPlayers, maximumNumberOfPlayers, required minimumDuration, maximumDuration, createdAt, updatedAt}): _name = name, _description = description, _minimumNumberOfPlayers = minimumNumberOfPlayers, _maximumNumberOfPlayers = maximumNumberOfPlayers, _minimumDuration = minimumDuration, _maximumDuration = maximumDuration, _createdAt = createdAt, _updatedAt = updatedAt;
  
  factory BoardGame({String? id, required String name, required String description, required int minimumNumberOfPlayers, int? maximumNumberOfPlayers, required int minimumDuration, int? maximumDuration}) {
    return BoardGame._internal(
      id: id == null ? UUID.getUUID() : id,
      name: name,
      description: description,
      minimumNumberOfPlayers: minimumNumberOfPlayers,
      maximumNumberOfPlayers: maximumNumberOfPlayers,
      minimumDuration: minimumDuration,
      maximumDuration: maximumDuration);
  }
  
  bool equals(Object other) {
    return this == other;
  }
  
  @override
  bool operator ==(Object other) {
    if (identical(other, this)) return true;
    return other is BoardGame &&
      id == other.id &&
      _name == other._name &&
      _description == other._description &&
      _minimumNumberOfPlayers == other._minimumNumberOfPlayers &&
      _maximumNumberOfPlayers == other._maximumNumberOfPlayers &&
      _minimumDuration == other._minimumDuration &&
      _maximumDuration == other._maximumDuration;
  }
  
  @override
  int get hashCode => toString().hashCode;
  
  @override
  String toString() {
    var buffer = new StringBuffer();
    
    buffer.write("BoardGame {");
    buffer.write("id=" + "$id" + ", ");
    buffer.write("name=" + "$_name" + ", ");
    buffer.write("description=" + "$_description" + ", ");
    buffer.write("minimumNumberOfPlayers=" + (_minimumNumberOfPlayers != null ? _minimumNumberOfPlayers!.toString() : "null") + ", ");
    buffer.write("maximumNumberOfPlayers=" + (_maximumNumberOfPlayers != null ? _maximumNumberOfPlayers!.toString() : "null") + ", ");
    buffer.write("minimumDuration=" + (_minimumDuration != null ? _minimumDuration!.toString() : "null") + ", ");
    buffer.write("maximumDuration=" + (_maximumDuration != null ? _maximumDuration!.toString() : "null") + ", ");
    buffer.write("createdAt=" + (_createdAt != null ? _createdAt!.format() : "null") + ", ");
    buffer.write("updatedAt=" + (_updatedAt != null ? _updatedAt!.format() : "null"));
    buffer.write("}");
    
    return buffer.toString();
  }
  
  BoardGame copyWith({String? name, String? description, int? minimumNumberOfPlayers, int? maximumNumberOfPlayers, int? minimumDuration, int? maximumDuration}) {
    return BoardGame._internal(
      id: id,
      name: name ?? this.name,
      description: description ?? this.description,
      minimumNumberOfPlayers: minimumNumberOfPlayers ?? this.minimumNumberOfPlayers,
      maximumNumberOfPlayers: maximumNumberOfPlayers ?? this.maximumNumberOfPlayers,
      minimumDuration: minimumDuration ?? this.minimumDuration,
      maximumDuration: maximumDuration ?? this.maximumDuration);
  }
  
  BoardGame.fromJson(Map<String, dynamic> json)  
    : id = json['id'],
      _name = json['name'],
      _description = json['description'],
      _minimumNumberOfPlayers = (json['minimumNumberOfPlayers'] as num?)?.toInt(),
      _maximumNumberOfPlayers = (json['maximumNumberOfPlayers'] as num?)?.toInt(),
      _minimumDuration = (json['minimumDuration'] as num?)?.toInt(),
      _maximumDuration = (json['maximumDuration'] as num?)?.toInt(),
      _createdAt = json['createdAt'] != null ? TemporalDateTime.fromString(json['createdAt']) : null,
      _updatedAt = json['updatedAt'] != null ? TemporalDateTime.fromString(json['updatedAt']) : null;
  
  Map<String, dynamic> toJson() => {
    'id': id, 'name': _name, 'description': _description, 'minimumNumberOfPlayers': _minimumNumberOfPlayers, 'maximumNumberOfPlayers': _maximumNumberOfPlayers, 'minimumDuration': _minimumDuration, 'maximumDuration': _maximumDuration, 'createdAt': _createdAt?.format(), 'updatedAt': _updatedAt?.format()
  };
  
  Map<String, Object?> toMap() => {
    'id': id, 'name': _name, 'description': _description, 'minimumNumberOfPlayers': _minimumNumberOfPlayers, 'maximumNumberOfPlayers': _maximumNumberOfPlayers, 'minimumDuration': _minimumDuration, 'maximumDuration': _maximumDuration, 'createdAt': _createdAt, 'updatedAt': _updatedAt
  };

  static final QueryModelIdentifier<BoardGameModelIdentifier> MODEL_IDENTIFIER = QueryModelIdentifier<BoardGameModelIdentifier>();
  static final QueryField ID = QueryField(fieldName: "id");
  static final QueryField NAME = QueryField(fieldName: "name");
  static final QueryField DESCRIPTION = QueryField(fieldName: "description");
  static final QueryField MINIMUMNUMBEROFPLAYERS = QueryField(fieldName: "minimumNumberOfPlayers");
  static final QueryField MAXIMUMNUMBEROFPLAYERS = QueryField(fieldName: "maximumNumberOfPlayers");
  static final QueryField MINIMUMDURATION = QueryField(fieldName: "minimumDuration");
  static final QueryField MAXIMUMDURATION = QueryField(fieldName: "maximumDuration");
  static var schema = Model.defineSchema(define: (ModelSchemaDefinition modelSchemaDefinition) {
    modelSchemaDefinition.name = "BoardGame";
    modelSchemaDefinition.pluralName = "BoardGames";
    
    modelSchemaDefinition.addField(ModelFieldDefinition.id());
    
    modelSchemaDefinition.addField(ModelFieldDefinition.field(
      key: BoardGame.NAME,
      isRequired: true,
      ofType: ModelFieldType(ModelFieldTypeEnum.string)
    ));
    
    modelSchemaDefinition.addField(ModelFieldDefinition.field(
      key: BoardGame.DESCRIPTION,
      isRequired: true,
      ofType: ModelFieldType(ModelFieldTypeEnum.string)
    ));
    
    modelSchemaDefinition.addField(ModelFieldDefinition.field(
      key: BoardGame.MINIMUMNUMBEROFPLAYERS,
      isRequired: true,
      ofType: ModelFieldType(ModelFieldTypeEnum.int)
    ));
    
    modelSchemaDefinition.addField(ModelFieldDefinition.field(
      key: BoardGame.MAXIMUMNUMBEROFPLAYERS,
      isRequired: false,
      ofType: ModelFieldType(ModelFieldTypeEnum.int)
    ));
    
    modelSchemaDefinition.addField(ModelFieldDefinition.field(
      key: BoardGame.MINIMUMDURATION,
      isRequired: true,
      ofType: ModelFieldType(ModelFieldTypeEnum.int)
    ));
    
    modelSchemaDefinition.addField(ModelFieldDefinition.field(
      key: BoardGame.MAXIMUMDURATION,
      isRequired: false,
      ofType: ModelFieldType(ModelFieldTypeEnum.int)
    ));
    
    modelSchemaDefinition.addField(ModelFieldDefinition.nonQueryField(
      fieldName: 'createdAt',
      isRequired: false,
      isReadOnly: true,
      ofType: ModelFieldType(ModelFieldTypeEnum.dateTime)
    ));
    
    modelSchemaDefinition.addField(ModelFieldDefinition.nonQueryField(
      fieldName: 'updatedAt',
      isRequired: false,
      isReadOnly: true,
      ofType: ModelFieldType(ModelFieldTypeEnum.dateTime)
    ));
  });
}

class _BoardGameModelType extends ModelType<BoardGame> {
  const _BoardGameModelType();
  
  @override
  BoardGame fromJson(Map<String, dynamic> jsonData) {
    return BoardGame.fromJson(jsonData);
  }
  
  @override
  String modelName() {
    return 'BoardGame';
  }
}

/**
 * This is an auto generated class representing the model identifier
 * of [BoardGame] in your schema.
 */
@immutable
class BoardGameModelIdentifier implements ModelIdentifier<BoardGame> {
  final String id;

  /** Create an instance of BoardGameModelIdentifier using [id] the primary key. */
  const BoardGameModelIdentifier({
    required this.id});
  
  @override
  Map<String, dynamic> serializeAsMap() => (<String, dynamic>{
    'id': id
  });
  
  @override
  List<Map<String, dynamic>> serializeAsList() => serializeAsMap()
    .entries
    .map((entry) => (<String, dynamic>{ entry.key: entry.value }))
    .toList();
  
  @override
  String serializeAsString() => serializeAsMap().values.join('#');
  
  @override
  String toString() => 'BoardGameModelIdentifier(id: $id)';
  
  @override
  bool operator ==(Object other) {
    if (identical(this, other)) {
      return true;
    }
    
    return other is BoardGameModelIdentifier &&
      id == other.id;
  }
  
  @override
  int get hashCode =>
    id.hashCode;
}